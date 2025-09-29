import hashlib
from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask import Response, json, jsonify, send_file, render_template_string
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
import matplotlib.pyplot as plt
import os
import io
import MySQLdb.cursors
import datetime
import calendar
from calendar import monthrange
import pandas as pd
import numpy as np
import functools
import pdfkit
import re
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import secrets, string

app = Flask(__name__)
app.secret_key = 'la nam'

UPLOAD_FOLDER = 'static/web'
UPLOAD_FOLDER_IMG = 'static/web/img'
SAVE_FOLDER_PDF = 'static/web/pdf'
SAVE_FOLDER_EXCEL = 'static/web/excel'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'quan_ly_nhan_su'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_IMG'] = UPLOAD_FOLDER_IMG
app.config['SAVE_FOLDER_PDF'] = SAVE_FOLDER_PDF
app.config['SAVE_FOLDER_EXCEL'] = SAVE_FOLDER_EXCEL
CAPTCHA_LEN = 5
CAPTCHA_EXPIRE_SECS = 180
mysql = MySQL(app)
def generate_captcha_text(length=CAPTCHA_LEN):
    # Loại bỏ ký tự dễ nhầm: 0/O, 1/I/L
    alphabet = ''.join(ch for ch in (string.ascii_uppercase + string.digits)
                       if ch not in {'0', 'O', '1', 'I', 'L'})
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def make_captcha_image(text):
    # Kích thước/đồ họa cơ bản
    width, height = 160, 56
    img = Image.new("RGB", (width, height), (245, 247, 250))
    draw = ImageDraw.Draw(img)

    # Font: nếu không có file .ttf, fallback default
    try:
        # Nếu sau này bạn thêm font .ttf: đặt ở static/fonts/Roboto-Bold.ttf
        font = ImageFont.truetype("static/fonts/Roboto-Bold.ttf", 34)
    except Exception:
        font = ImageFont.load_default()

    # Vẽ một vài đường nhiễu
    for _ in range(3):
        x1 = secrets.randbelow(width)
        y1 = secrets.randbelow(height)
        x2 = secrets.randbelow(width)
        y2 = secrets.randbelow(height)
        draw.line([(x1, y1), (x2, y2)], fill=(180, 185, 190), width=2)

    # Vẽ từng ký tự với lệch vị trí nhẹ
    padding_x = 14
    for i, ch in enumerate(text):
        # jitter vị trí
        off_x = padding_x + i * 26 + secrets.randbelow(6) - 3
        off_y = 10 + secrets.randbelow(8) - 4
        draw.text((off_x, off_y), ch, font=font, fill=(40, 40, 40))

    # Thêm chấm nhiễu
    for _ in range(150):
        x = secrets.randbelow(width)
        y = secrets.randbelow(height)
        img.putpixel((x, y), (secrets.randbelow(120) + 100,
                              secrets.randbelow(120) + 100,
                              secrets.randbelow(120) + 100))

    # Filter nhẹ để phá OCR
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

    # Xuất PNG vào buffer
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf
def login_required(func): # need for some router
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)

    return secure_function
    
@app.route("/logout")
def logout():
    if 'chamcong' in session.keys():
        form_add_data_cham_cong()
    
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
@app.route("/login", methods=['GET','POST'])
def login():
    if 'username' in session.keys():
        return redirect(url_for("home"))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM qlnv_congty")
    congty = cur.fetchall()[0]
    
    if 'congty' not in session.keys():
        session['congty'] = congty
    
    if request.method == 'POST':
        details = request.form
        captcha_input = details.get('captcha', '').strip()
        captcha_true = session.get('captcha_text')
        captcha_time = session.get('captcha_time')
        now_ts = datetime.datetime.utcnow().timestamp()

        # Hết hạn hoặc sai → báo lỗi + render lại
        if (not captcha_true) or (not captcha_time) or (now_ts - float(captcha_time) > CAPTCHA_EXPIRE_SECS) \
           or (captcha_input.upper() != str(captcha_true).upper()):
            return render_template('general/login.html',
                                   congty=session['congty'],
                                   captcha_err='True')
        user_name = details['username'].strip()
        password = hashlib.md5(details['current-password'].encode()).hexdigest()
        
        cur.execute("""SELECT us.*, img.PathToImage
                FROM qlnv_user us
                JOIN qlnv_nhanvien nv ON us.MaNhanVien = nv.MaNhanVien
                JOIN qlnv_imagedata img ON nv.ID_profile_image = img.ID_image
                WHERE username=%s""",(user_name,))
        user_data = cur.fetchall()
        
        if len(user_data)==0:
            return render_template('general/login.html',
                                   congty = session['congty'],
                                   user_exits='False',
                                   pass_check='False')
        
        if password != user_data[0][2]:
            return render_template('general/login.html', 
                                   congty = session['congty'],
                                   user_exits='True', 
                                   pass_check='False')
    
        my_user = user_data[0]
        
        cur.execute("""
            SELECT MaPhongBan
            FROM qlnv_nhanvien
            WHERE MaNhanVien = %s
            """, (my_user[4],))
        maPB = cur.fetchall()[0][0]
        
        elms = list(my_user)
        elms.append(maPB)
        my_user = elms
        
        cur.execute("""
                    UPDATE `qlnv_user` 
                    SET `LastLogin` = CURRENT_TIMESTAMP()
                    WHERE `qlnv_user`.`Id_user` = %s
                    """, (my_user[0],))
        session['username'] = my_user
        mysql.connection.commit()
        
        cur.execute("""
                SELECT r.role_folder
                FROM qlnv_role r
                JOIN qlnv_phanquyenuser pq ON pq.role_id = r.role_id
                WHERE pq.id_user = %s
            """, (my_user[0], ))
        role = cur.fetchall()[0][0]
        session['role'] = role
        
        cur.execute("""
                SELECT r.role_id
                FROM qlnv_role r
                JOIN qlnv_phanquyenuser pq ON pq.role_id = r.role_id
                WHERE pq.id_user = %s
            """, (my_user[0], ))
        role_id = cur.fetchall()[0][0]
        session['role_id'] = role_id
        
        cur.close()
        session.pop('captcha_text', None)
        session.pop('captcha_time', None)
        return redirect(url_for("home"))
    return render_template('general/login.html',
                           congty = session['congty'])
@app.route("/captcha.png")
def captcha_png():
    # Sinh chuỗi + lưu đáp án & timestamp vào session
    text = generate_captcha_text()
    session['captcha_text'] = text
    session['captcha_time'] = datetime.datetime.utcnow().timestamp()

    # Tạo ảnh và trả về
    img_buf = make_captcha_image(text)
    resp = Response(img_buf.getvalue(), mimetype="image/png")
    # No-cache để luôn hiện ảnh mới
    resp.headers["Cache-Control"] = "no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp
#thêm chức năng đang ký tài khoản cho người dùng thường nha (kh phân quyền)
@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for("home"))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM qlnv_congty")
    congty = cur.fetchall()[0] if cur.rowcount > 0 else None
    if 'congty' not in session and congty:
        session['congty'] = congty

    cur.execute("""
        SELECT MaNhanVien, TenNV
        FROM qlnv_nhanvien
        WHERE MaNhanVien NOT IN (
            SELECT DISTINCT us.MaNhanVien
            FROM qlnv_user us
        )
    """)
    nhanvien = cur.fetchall()

    type_account = {
        'Admin': 1,
        'Trưởng Phòng': 2,
        'Nhân Viên': 3
    }

    if request.method == 'POST':
        details = request.form
        username = details.get('username', '').strip()
        password = details.get('password', '')
        confirm = details.get('confirm_password', '')
        manv = details.get('manv', '').strip() 
        loai_tk = details.get('type', 'Nhân Viên') 

        if not username or not password:
            return render_template('general/register.html',
                                   congty=session.get('congty'),
                                   error="Vui lòng nhập đầy đủ username và password",
                                   nhanvien=nhanvien,
                                   type_account=list(type_account.keys()),
                                   form=details)

        if password != confirm:
            return render_template('general/register.html',
                                   congty=session.get('congty'),
                                   error="Mật khẩu nhập lại không khớp",
                                   nhanvien=nhanvien,
                                   type_account=list(type_account.keys()),
                                   form=details)
        cur.execute("SELECT Id_user FROM qlnv_user WHERE username = %s", (username,))
        if cur.fetchone():
            return render_template('general/register.html',
                                   congty=session.get('congty'),
                                   error="Username đã tồn tại",
                                   nhanvien=nhanvien,
                                   type_account=list(type_account.keys()),
                                   form=details)

        password_hashed = hashlib.md5(password.encode()).hexdigest()

        try:
            if not manv:
                cur.execute("SELECT MaNhanVien FROM qlnv_nhanvien")
                rows = cur.fetchall()
                max_num = 0
                chosen_prefix = "MNV"
                chosen_width = 2

                for r in rows:
                    code = r[0]
                    if not code:
                        continue
                    m = re.search(r'(\d+)$', str(code))
                    if m:
                        num = int(m.group(1))
                        if num > max_num:
                            max_num = num
                            chosen_width = max(chosen_width, len(m.group(1)))
                            chosen_prefix = code[:m.start(1)]

                if max_num == 0:
                    manv = f"{chosen_prefix}01" if chosen_prefix else "MNV01"
                else:
                    manv = f"{chosen_prefix}{(max_num + 1):0{chosen_width}d}"
                cur.execute("""
                    INSERT INTO qlnv_nhanvien (MaNhanVien, TenNV)
                    VALUES (%s, %s)
                """, (manv, username))
                mysql.connection.commit()
            else:
                cur.execute("SELECT MaNhanVien FROM qlnv_nhanvien WHERE MaNhanVien = %s", (manv,))
                if not cur.fetchone():
                    return render_template('general/register.html',
                                           congty=session.get('congty'),
                                           error="Mã nhân viên không tồn tại",
                                           nhanvien=nhanvien,
                                           type_account=list(type_account.keys()),
                                           form=details)
            cur.execute("""
                INSERT INTO qlnv_user (Id_user, username, password, tennguoidung, MaNhanVien, LastLogin, register)
                VALUES (NULL, %s, %s, %s, %s, NULL, current_timestamp())
            """, (username, password_hashed, username, manv))
            mysql.connection.commit()
            cur.execute("SELECT Id_user FROM qlnv_user WHERE username = %s", (username,))
            acc = cur.fetchone()
            if acc:
                acc_id = acc[0]
                role_id = type_account.get(loai_tk, 3)
                cur.execute("INSERT INTO qlnv_phanquyenuser(id_user, role_id) VALUES (%s, %s)", (acc_id, role_id))
                mysql.connection.commit()

            cur.close()
            return redirect(url_for('login'))

        except Exception as e:
            try:
                mysql.connection.rollback()
            except:
                pass
            cur.close()
            return render_template('general/register.html',
                                   congty=session.get('congty'),
                                   error=f"Lỗi khi lưu dữ liệu: {str(e)}",
                                   nhanvien=nhanvien,
                                   type_account=list(type_account.keys()),
                                   form=details)
    return render_template('general/register.html',
                           congty=session.get('congty'),
                           nhanvien=nhanvien,
                           type_account=list(type_account.keys()))

@app.route("/home")
def home():
    if 'username' in session.keys():
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM qlnv_nhanvien")
        num_nv = cur.fetchall()[0][0]
        
        cur.execute("SELECT COUNT(*) FROM qlnv_phongban")
        num_pb = cur.fetchall()[0][0]
        
        
        
        return render_template(session['role'] + 'index.html',
                               num_nv = num_nv,
                               num_pb = num_pb,
                               congty = session['congty'],
                               my_user = session['username'])
    return redirect(url_for("login"))

@app.route("/forgot")
def forgot():
    return render_template('general/forgot.html', 
                           congty = session['congty'])

#
# ------------------ EMPLOYEES ------------------------
#
@login_required
@app.route("/table_data_employees")
def table_data_employees():
    
    if session['role_id'] != 1:
        abort(404)
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT nv.MaNhanVien, nv.TenNV, img.PathToImage, nv.DiaChi, DATE_FORMAT(nv.NgaySinh,"%d-%m-%Y"), nv.GioiTinh, nv.DienThoai, cv.TenCV
        FROM qlnv_nhanvien nv
        JOIN qlnv_chucvu cv ON nv.MaChucVu = cv.MaCV
        JOIN qlnv_imagedata img ON nv.ID_profile_image = img.ID_image""")
    nhanvien = cur.fetchall()
    cur.close()
    return render_template(session['role'] + 'employees/table_data_employees.html',
                           nhanvien = nhanvien,
                           congty = session['congty'],
                           my_user = session['username'])

@login_required
@app.route("/form_add_data_employees", methods=['GET','POST'])
def form_add_data_employees():
    
    if session['role_id'] != 1:
        abort(404)
    
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM qlnv_chucvu""")
    chucvu = cur.fetchall()
    
    cur.execute("""SELECT * FROM qlnv_trinhdohocvan""")
    trinhdohocvan = cur.fetchall()
    
    cur.execute("""SELECT * FROM qlnv_phongban""")
    phongban = cur.fetchall()
    
    if request.method == 'POST':
        details = request.form
        MNV = details['MNV'].strip()
        TENNV = details['TENNV'].strip()
        MAIL = details['MAIL'].strip()
        DIACHI = details['DIACHI'].strip()
        SDT = details['SDT'].strip()
        BHYT = details['BHYT'].strip()
        BHXH = details['BHXH'].strip()
        NGAYSINH = details['NGAYSINH'].strip()
        NOISINH = details['NOISINH'].strip()
        CMND = details['CMND'].strip()
        NGAYCMND = details['NGAYCMND'].strip()
        NOICMND = details['NOICMND'].strip()
        GIOITINH = details['GIOITINH'].strip()
        MATDHV = details['MATDHV'].strip().split(" - ")[0]
        HONHAN = details['HONHAN'].strip()
        LUONG = details['LUONG'].strip()
        MAHD = details['MAHD'].strip()
        DANTOC = details['DANTOC']
        CV = details['CV'].strip()
        PB = details['MAPB'].strip()
        ID_image = "none_image_profile"
        
        cur.execute("""SELECT MaNhanVien FROM qlnv_nhanvien WHERE MaNhanVien=%s""", (MNV, ))
        kiem_tra_ma_nhan_vien = cur.fetchall()
        
        if len(kiem_tra_ma_nhan_vien) != 0:
            return render_template(session['role'] +'employees/form_add_data_employees.html',
                        ma_err="True",
                        trinhdohocvan = trinhdohocvan, 
                        chucvu = chucvu,
                        phongban = phongban,
                        congty = session['congty'],
                        my_user = session['username'])
        
        for data in chucvu:
            if (CV in data):
                CV = data[0]
                break;
        
        for data in phongban:
            if (PB in data):
                PB = data[0]
                break;
        
        image_profile = request.files['ImageProfileUpload']
        
        if image_profile.filename != '':
            ID_image = "Image_Profile_" + MNV 
            filename = ID_image + "." + secure_filename(image_profile.filename).split(".")[1]
            pathToImage = app.config['UPLOAD_FOLDER_IMG'] + "/" + filename
            image_profile.save(pathToImage)
            take_image_to_save(ID_image, pathToImage)
        
        cur.execute("""INSERT INTO `qlnv_nhanvien` 
            (MaNhanVien, MaChucVu, MaPhongBan,
            Luong, GioiTinh, MaHD, TenNV,
            NgaySinh, NoiSinh, SoCMT, DienThoai,
            DiaChi, Email, TTHonNhan, DanToc,
            MATDHV, NgayCMND, NoiCMND, BHYT, BHXH, ID_profile_image)
            VALUES
            (%s, %s, %s, %s, %s, %s,
             %s, %s, %s, %s, %s, %s,
             %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (MNV, CV, PB, LUONG, GIOITINH, MAHD,
            TENNV, NGAYSINH, NOISINH, CMND, SDT, DIACHI,
            MAIL, HONHAN, DANTOC, MATDHV, NGAYCMND, NOICMND, BHYT, BHXH, ID_image))
        
        cur.execute("""INSERT INTO qlnv_thoigiancongtac(MaNV, MaCV, NgayNhanChuc, NgayKetThuc, DuongNhiem)
                    VALUES (%s, %s, CURRENT_DATE(), NULL, '1')
                    """, (MNV, CV))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("table_data_employees"))
    return render_template(session['role'] +'employees/form_add_data_employees.html',
                           trinhdohocvan = trinhdohocvan, 
                           chucvu = chucvu,
                           phongban = phongban,
                           congty = session['congty'],
                           my_user = session['username'])
    
@login_required
@app.route("/form_view_update_employees/<string:maNV>_<string:canEdit>", methods=['GET','POST'])
def form_view_update_employees(maNV, canEdit):
    
    if session['role_id'] != 1:
        if (session['username'][4] != maNV):
            abort(404)
    
    mode = "disabled"
    if (canEdit == "Y"):
        mode = "";
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT nv.MaNhanVien, nv.TenNV, nv.GioiTinh, nv.NgaySinh, nv.DanToc,
        nv.SoCMT, nv.NgayCMND, nv.NoiCMND, nv.DienThoai, nv.Email, nv.DiaChi,
        nv.NoiSinh, nv.BHYT, NV.BHXH, img.PathToImage, pb.TenPB, cv.TenCV,
        nv.MaHD, nv.Luong, nv.TTHonNhan, concat(hv.MATDHV, " - ", hv.TenTDHV," - " , hv.ChuyenNganh),
        nv.MaChucVu, nv.MaPhongBan, nv.MATDHV, img.ID_image
        FROM qlnv_nhanvien nv
        LEFT JOIN qlnv_imagedata img ON nv.ID_profile_image = img.ID_image
        LEFT JOIN qlnv_phongban pb ON nv.MaPhongBan = pb.MaPB
        LEFT JOIN qlnv_chucvu cv ON nv.MaChucVu = cv.MaCV
        LEFT JOIN qlnv_trinhdohocvan hv ON nv.MATDHV = hv.MATDHV
        WHERE nv.MaNhanVien = %s
                """, (maNV, ))
    data_default = cur.fetchall()
    
    if (len(data_default) != 1): # Need page error
        abort(404)
    data_default = data_default[0]
    
    cur.execute("""SELECT * FROM qlnv_chucvu WHERE MaCV != %s""", (data_default[21], ))
    chucvu = cur.fetchall()
    
    if data_default[23] != None:
        cur.execute("""SELECT * FROM qlnv_trinhdohocvan WHERE MATDHV != %s""", (data_default[23], ))
        trinhdohocvan = cur.fetchall()
    else:
        cur.execute("""SELECT * FROM qlnv_trinhdohocvan""")
        trinhdohocvan = cur.fetchall()
    
    cur.execute("""SELECT * FROM qlnv_phongban WHERE MaPB != %s""", (data_default[22], ))
    phongban = cur.fetchall()
    
    if request.method == 'POST':
        details = request.form
        MNV = maNV
        TENNV = details['TENNV'].strip()
        MAIL = details['MAIL'].strip()
        DIACHI = details['DIACHI'].strip()
        SDT = details['SDT'].strip()
        BHYT = details['BHYT'].strip()
        BHXH = details['BHXH'].strip()
        NGAYSINH = details['NGAYSINH'].strip()
        NOISINH = details['NOISINH'].strip()
        CMND = details['CMND'].strip()
        NGAYCMND = details['NGAYCMND'].strip()
        NOICMND = details['NOICMND'].strip()
        GIOITINH = details['GIOITINH'].strip()
        MATDHV = details['MATDHV'].strip().split(" - ")[0]
        HONHAN = details['HONHAN'].strip()
        LUONG = data_default[18]
        MAHD = data_default[17]
        CV = data_default[16]
        PB = data_default[15]
        DANTOC = details['DANTOC'].strip()
        ID_image = data_default[24]
        
        if session['role_id'] == 1:
            LUONG = details['LUONG'].strip()
            MAHD = details['MAHD'].strip()
            CV = details['CV'].strip()
            PB = details['MAPB'].strip()
        
        if (CV != data_default[16]):
            for data in chucvu:
                if (CV in data):
                    CV = data[0]
                    break;
        else:
            CV = data_default[21]
        
        if (PB != data_default[15]):
            for data in phongban:
                if (PB in data):
                    PB = data[0]
                    break;
        else:
            PB = data_default[22]
        
        image_profile = request.files['ImageProfileUpload']
        
        if image_profile.filename != "":
            ID_image = "Image_Profile_" + MNV 
            filename = ID_image + "." + secure_filename(image_profile.filename).split(".")[1]
            pathToImage = app.config['UPLOAD_FOLDER_IMG'] + "/" + filename
            image_profile.save(pathToImage)
            take_image_to_save(ID_image, pathToImage)
        
        cur.execute("""UPDATE qlnv_nhanvien
            SET MaChucVu = %s, MaPhongBan = %s,
            Luong= %s, GioiTinh= %s, MaHD= %s, TenNV= %s,
            NgaySinh= %s, NoiSinh= %s, SoCMT= %s, DienThoai= %s,
            DiaChi= %s, Email= %s, TTHonNhan= %s, DanToc= %s,
            MATDHV= %s, NgayCMND= %s, NoiCMND= %s, BHYT= %s,
            BHXH= %s, ID_profile_image= %s
            WHERE MaNhanVien = %s""",
            (CV, PB, LUONG, GIOITINH, MAHD,
            TENNV, NGAYSINH, NOISINH, CMND, SDT, DIACHI,
            MAIL, HONHAN, DANTOC, MATDHV, NGAYCMND, NOICMND, BHYT, BHXH, ID_image, MNV))
        mysql.connection.commit()
        
        if (maNV == session['username'][4]):
                cur.execute("""SELECT us.*, img.PathToImage
                FROM qlnv_user us
                JOIN qlnv_nhanvien nv ON us.MaNhanVien = nv.MaNhanVien
                JOIN qlnv_imagedata img ON nv.ID_profile_image = img.ID_image
                WHERE username=%s""",(session['username'][1],))
                user_data = cur.fetchall()
                
                my_user = user_data[0]
        
                cur.execute("""
                    SELECT MaPhongBan
                    FROM qlnv_nhanvien
                    WHERE MaNhanVien = %s
                    """, (my_user[4],))
                maPB = cur.fetchall()[0][0]
                
                elms = list(my_user)
                elms.append(maPB)
                my_user = elms
                session['username'] = my_user
                
        
        cur.close()
        if session['role_id'] != 1:
            return redirect(url_for("form_view_update_employees", maNV = maNV, canEdit = 'N'))
        return redirect(url_for("table_data_employees"))
    return render_template(session['role'] +'employees/form_view_update_employees.html',
                           mode=mode,
                           data_default = data_default,
                           trinhdohocvan = trinhdohocvan, 
                           chucvu = chucvu,
                           phongban = phongban,
                           congty = session['congty'],
                           my_user = session['username'])
    



@login_required
@app.route("/form_add_data_employees_upload_process/<string:filename>", methods=['GET','POST'])
def form_add_data_employees_upload_process(filename):
    if session['role_id'] != 1:
        abort(404)
    
    pathToFile = app.config['UPLOAD_FOLDER'] + "/" + filename
    
    default_tag_Column = ['MaNhanVien', 'MaChucVu', 'MaPhongBan',
                    'Luong', 'GioiTinh', 'MaHD', 'TenNV',
                    'NgaySinh', 'NoiSinh', 'SoCMT', 'DienThoai',
                    'DiaChi', 'Email', 'TTHonNhan', 'DanToc',
                    'MATDHV', 'NgayCMND', 'NoiCMND', 'BHYT', 'BHXH']
    
    default_name_Column = ['Mã nhân viên', 'Chức vụ', 'Phòng Ban', 'Lương', 'Giới tính',
                           'Mã Hợp đồng', 'Tên Nhân Viên', 'Ngày Sinh',  'Nơi sinh', 'Chứng minh thư (thẻ căn cước)',
                           'Số điện thoại', 'Địa Chỉ', 'Email', 'Tình trạng hôn nhân', 'Dân tộc',
                           'Trình Độ Học Vấn', 'Ngày cấp CMND', 'Nơi cấp CMND', 'Bảo hiểm y tế', 'Bảo hiểm xã hội']
    
    data_nv = pd.read_excel(pathToFile)
    data_column = list(data_nv.columns)
    
    if (len(data_column) > len(default_tag_Column)) or len(data_column) < 3:
        abort(404)
    
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        details = request.form
        column_link = [details[col] for col in data_column]
        column_match = [default_name_Column.index(elm) for elm in column_link]
        
        if (len(set(column_match)) != len(column_link)):
            abort(404)
        
        if 0 not in column_match or 1 not in column_match or 2 not in column_match:
            abort(404)
    
        # convert Ten CV to ChucVu
        tmp = tuple(set(data_nv[data_column[column_match.index(1)]]))
        if len(tmp) == 1:
            cur.execute("SELECT MaCV FROM qlnv_chucvu WHERE TenCV = %s", tmp)
        else:
            new_tmp = ["\"" + text +"\"" for text in tmp]
            cur.execute("SELECT MaCV FROM qlnv_chucvu WHERE TenCV IN (" + ", ".join(new_tmp) + ")")
        data_tuple = cur.fetchall()
        data_tmp_take = []
        for elm in data_tuple:
            data_tmp_take.append(elm[0])
        if (len(data_tmp_take) != len(tmp)):
            abort(404)
        data_nv[data_column[column_match.index(1)]] = data_nv[data_column[column_match.index(1)]].replace(list(tmp), data_tmp_take)

        # convert Ten PB to PhongBan
        tmp = tuple(set(data_nv[data_column[column_match.index(2)]]))
        if len(tmp) == 1:
            cur.execute("SELECT MaPB FROM qlnv_phongban WHERE TenPB = %s", tmp)
        else:
            new_tmp = ["\"" + text +"\"" for text in tmp]
            cur.execute("SELECT MaPB FROM qlnv_phongban WHERE TenPB IN (" + ", ".join(new_tmp) + ")")
        data_tuple = cur.fetchall()
        data_tmp_take = []
        for elm in data_tuple:
            data_tmp_take.append(elm[0])
        if (len(data_tmp_take) != len(tmp)):
            abort(404)
        data_nv[data_column[column_match.index(2)]] = data_nv[data_column[column_match.index(2)]].replace(list(tmp), data_tmp_take)
        
        # Chuyển đổi trình độ học vấn
        if 15 in column_match:
            tdhv_cn = set(data_nv[data_column[column_match.index(15)]]) # Trình dộ học vấn - chuyên ngành
            tmp = []
            sql_find_tdhv = "SELECT td.MATDHV FROM qlnv_trinhdohocvan td WHERE "
            for elm in tdhv_cn:
                sql_find_tdhv += " ( td.TenTDHV = %s AND td.ChuyenNganh = %s ) OR"
                new_tmp = [text.strip() for text in elm.split("-")]
                tmp += new_tmp
            sql_find_tdhv = sql_find_tdhv[:-2:]
            cur.execute(sql_find_tdhv, tuple(tmp))
            data_tdhv = cur.fetchall()
            data_tdhv_lst = []
            for elm in data_tdhv:
                data_tdhv_lst.append(elm[0])
            if (len(tdhv_cn) != len(data_tdhv_lst)):
                abort(404)
            data_nv[data_column[column_match.index(15)]] = data_nv[data_column[column_match.index(15)]].replace(list(tdhv_cn), data_tdhv)
        
        sql = "INSERT INTO `qlnv_nhanvien` ("
        for index in column_match:
            sql += default_tag_Column[index] + ","
        sql = sql[:-1:]
        sql += ") VALUES "
        for index_row in range(data_nv.shape[0]):
            sql += "("
            for col in data_column:
                sql +=  "\"" + str(data_nv[col][index_row]) + "\"" + ","
            sql = sql[:-1:]
            sql += "),"
        sql = sql[:-1:]    
        
        cur.execute(sql)
        mysql.connection.commit()
        cur.close()
        os.remove(pathToFile)
        return redirect(url_for('table_data_employees'))
    
    return render_template(session['role'] +"employees/form_add_data_employees_upload_process.html",
                           filename = filename,
                           congty = session['congty'],
                           my_user = session['username'],
                           name_column = default_name_Column,
                           index_column = data_column)


@login_required
@app.route("/get_information_one_employee/<string:maNV>")
def get_infomation_one_employee(maNV):
    
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT nv.MaNhanVien, nv.TenNV, nv.GioiTinh, DATE_FORMAT(nv.NgaySinh,"%d-%m-%Y"), nv.DanToc,
        nv.SoCMT, nv.NgayCMND, nv.NoiCMND, nv.DienThoai, nv.Email, nv.DiaChi, 
        nv.NoiSinh, nv.BHYT, NV.BHXH, img.PathToImage, pb.TenPB, cv.TenCV,
        nv.MaHD, nv.Luong, nv.TTHonNhan, concat(hv.TenTDHV," - " , hv.ChuyenNganh),
        nv.MaChucVu, nv.MaPhongBan, nv.MATDHV, img.ID_image, hd.LoaiHopDong
        FROM qlnv_nhanvien nv
        LEFT JOIN qlnv_imagedata img ON nv.ID_profile_image = img.ID_image
        LEFT JOIN qlnv_phongban pb ON nv.MaPhongBan = pb.MaPB
        LEFT JOIN qlnv_chucvu cv ON nv.MaChucVu = cv.MaCV
        LEFT JOIN qlnv_hopdong hd ON hd.MaHopDong = nv.MaHD
        LEFT JOIN qlnv_trinhdohocvan hv ON nv.MATDHV = hv.MATDHV
        WHERE nv.MaNhanVien = \"""" + maNV + "\"" )
    nhanvien = cur.fetchall()
    if (len(nhanvien) != 1):
        abort(404)
    
    cur.execute("""
                SELECT tg.id, tg.MaNV, cv.TenCV, tg.NgayNhanChuc, tg.NgayKetThuc, tg.DuongNhiem
                FROM qlnv_thoigiancongtac tg
                JOIN qlnv_chucvu cv ON tg.MaCV = cv.MaCV
                WHERE tg.MaNV = %s
                ORDER BY tg.NgayNhanChuc DESC
                """, (maNV, ))
    thoigiancongtac = cur.fetchall()
    
    
    cur.execute("""
                SELECT * FROM qlnv_congty
                """)
    congty = cur.fetchall()[0]
    cur.close()
    
    return render_template("employees/form_information_one_employee.html",
                           thoigiancongtac = thoigiancongtac,
                           congty = congty,
                           nhanvien = nhanvien[0])
    
    
@login_required
@app.route("/delete_nhan_vien/<string:maNV>")
def delete_nhan_vien(maNV):
    if session['role_id'] != 1:
        abort(404)
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT ID_profile_image FROM qlnv_nhanvien WHERE MaNhanVien=%s", (maNV, ))
    id_image = cur.fetchall()[0][0]
    
    if (id_image != "none_image_profile"):
        cur.execute("SELECT * FROM qlnv_imagedata WHERE ID_image=%s", (id_image, ))
        image_path = "static/" + cur.fetchall()[0][1]
        if os.path.exists(image_path):
            os.remove(image_path)
        cur.execute("DELETE FROM qlnv_imagedata WHERE ID_image=%s", (id_image, ))
    
    sql = "DELETE FROM qlnv_nhanvien WHERE MaNhanVien=%s"
    val = (maNV, )
    cur.execute(sql,val)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("table_data_employees"))
#
# ------------------ EMPLOYEES ------------------------
#

#
# ------------------ Trình độ học vấn ------------------------
#
@login_required
@app.route("/form_add_trinhdohocvan", methods=['GET','POST'])
def form_add_trinhdohocvan():
    if session['role_id'] != 1:
        abort(404)
    
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM qlnv_trinhdohocvan""")
    trinhdohocvan = cur.fetchall()
    
    if request.method == 'POST':
        details = request.form
        MATDHV = details['MATDHV'].strip()
        TenTDHV = details["TenTDHV"].strip()
        ChuyenNganh = details['ChuyenNganh'].strip()
        for data in trinhdohocvan:
            if (MATDHV in data):
                return render_template(session['role'] +"form_add_trinhdohocvan.html", 
                                       ma_err = "True", 
                                       congty = session['congty'],
                                       my_user = session['username'])
        
        cur.execute("INSERT INTO qlnv_trinhdohocvan(MATDHV, TenTDHV, ChuyenNganh) VALUES (%s, %s, %s)",
                    (MATDHV, TenTDHV, ChuyenNganh))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for("table_trinh_do_hoc_van"))
    return render_template(session['role'] +"trinhdohocvan/form_add_trinhdohocvan.html", 
                           congty = session['congty'],
                           my_user = session['username'])

@login_required
@app.route("/table_trinh_do_hoc_van")
def table_trinh_do_hoc_van():
    if session['role_id'] != 1:
        abort(404)
    
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT hv.*, COUNT(nv.MaNhanVien)
                FROM qlnv_trinhdohocvan hv
                LEFT JOIN qlnv_nhanvien nv ON hv.MATDHV = nv.MATDHV
                GROUP BY hv.MATDHV
                """)
    trinhdohocvan = cur.fetchall()
    cur.close()
    return render_template(session['role'] +"trinhdohocvan/table_trinh_do_hoc_van.html", 
                           trinhdohocvan = trinhdohocvan,
                           congty = session['congty'],
                           my_user = session['username'])
    
@login_required
@app.route("/form_view_update_trinh_do_hoc_van/<string:mode>_<string:maTDHV>", methods=['GET','POST'])
def form_view_update_trinh_do_hoc_van(mode, maTDHV):
    if session['role_id'] != 1:
        abort(404)
        
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT *
                FROM qlnv_trinhdohocvan
                """)
    trinhdohocvan = cur.fetchall()
    
    if request.method == 'POST':
        details = request.form
        MATDHV = details['MATDHV'].strip()
        TenTDHV = details["TenTDHV"].strip()
        ChuyenNganh = details['ChuyenNganh'].strip()
        
        if (MATDHV != maTDHV):
            cur.execute("""
                UPDATE qlnv_nhanvien
                SET MATDHV = %s
                WHERE MATDHV = %s
                """, (MATDHV, maTDHV))
        
        cur.execute("""
            UPDATE qlnv_trinhdohocvan
            SET MATDHV = %s, TenTDHV = %s, ChuyenNganh = %s
            WHERE MATDHV = %s
            """, (MATDHV, TenTDHV, ChuyenNganh, maTDHV))
        mysql.connection.commit()
        return redirect(url_for('table_trinh_do_hoc_van'))
    
    if (mode == "E"):
        cur.execute("""
        SELECT *
        FROM qlnv_trinhdohocvan
        WHERE maTDHV = %s""", (maTDHV, ))
        trinhdohocvan = cur.fetchall()
        
        if (len(trinhdohocvan) == 0):
            abort(404)
        
        return render_template(session['role'] +"trinhdohocvan/form_view_update_trinh_do_hoc_van.html", 
                                edit_view = mode,
                                maTDHV = maTDHV,
                                trinhdohocvan = trinhdohocvan[0],
                                congty = session['congty'],
                                my_user = session['username'])
    
    cur.close()
    return render_template(session['role'] +"trinhdohocvan/form_view_update_trinh_do_hoc_van.html", 
                           trinhdohocvan = trinhdohocvan,
                           congty = session['congty'],
                           my_user = session['username'])

@login_required
@app.route("/table_trinh_do_hoc_van/<string:maTDHV>")
def table_trinh_do_hoc_van_one(maTDHV):
    if session['role_id'] != 1:
        abort(404)
    
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT *
                FROM qlnv_trinhdohocvan
                WHERE MATDHV = %s
                """, (maTDHV, ))
    tenTDHV = cur.fetchall()
    if (len(tenTDHV) == 0):
        abort(404)
    tenTDHV = tenTDHV[0]
        
    cur.execute("""
                SELECT nv.MaNhanVien, nv.TenNV, DATE_FORMAT(nv.NgaySinh,"%d-%m-%Y"), nv.DienThoai, hv.TenTDHV, HV.ChuyenNganh
                FROM qlnv_trinhdohocvan hv
                JOIN qlnv_nhanvien nv ON hv.MATDHV = nv.MATDHV
                WHERE hv.MATDHV = \"""" + maTDHV + "\"") 
    trinhdohocvan = cur.fetchall()
    cur.close()
    
    if len(trinhdohocvan) == 0:
        abort(404)
    
    return render_template(session['role'] +"trinhdohocvan/table_trinh_do_hoc_van_nhan_vien.html", 
                           tenTDHV = tenTDHV,
                           trinhdohocvan = trinhdohocvan,
                           congty = session['congty'],
                           my_user = session['username'])
    
@login_required
@app.route("/delete_trinh_do_hoc_van/<string:maTDHV>")
def delete_trinh_do_hoc_van(maTDHV):
    if session['role_id'] != 1:
        abort(404)
    
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT COUNT(*)
                FROM qlnv_trinhdohocvan hv
                JOIN qlnv_nhanvien nv ON hv.MATDHV = nv.MATDHV
                WHERE hv.MATDHV = \"""" + maTDHV + "\"") 
    trinhdohocvan = cur.fetchall()[0][0]
    
    if trinhdohocvan != 0:
        abort(404)

    sql = "DELETE FROM qlnv_trinhdohocvan WHERE MATDHV=%s"
    val = (maTDHV, )
    cur.execute(sql,val)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('table_trinh_do_hoc_van'))


#
# ------------------ Trình độ học vấn ------------------------
#

#
# ------------------ CHUC VU ------------------------
#
@login_required
@app.route("/table_chuc_vu")
def table_chuc_vu():
    if session['role_id'] != 1:
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT cv.MaCV, cv.TenCV, COUNT(NV.MaNhanVien) 
        FROM qlnv_chucvu cv
        LEFT JOIN qlnv_nhanvien nv ON cv.MaCV = nv.MaChucVu
        LEFT JOIN qlnv_thoigiancongtac tg ON tg.MaNV = nv.MaNhanVien
        WHERE tg.DuongNhiem = 1 
        GROUP BY cv.MaCV""")
    chucvu = cur.fetchall()
    cur.close()
    return render_template(session['role'] +"chucvu/table_chuc_vu.html",
                           chucvu = chucvu,
                           congty = session['congty'],
                           my_user = session['username'])
    
@login_required
@app.route("/form_view_update_chuc_vu/<string:mode>_<string:maCV>", methods=['GET','POST'])
def form_view_update_chuc_vu(mode, maCV):
    if session['role_id'] != 1:
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT *
        FROM qlnv_chucvu """)
    chucvu = cur.fetchall()
    
    if request.method == 'POST':
        details = request.form
        MaCV = details['MaCV'].strip()
        TenCV = details["TenCV"].strip()
        
        if (MaCV != maCV):
            cur.execute("""
                UPDATE qlnv_nhanvien
                SET MaChucVu = %s
                WHERE MaChucVu = %s
                """, (MaCV, maCV))
        
        cur.execute("""
            UPDATE qlnv_chucvu
            SET MaCV = %s, TenCV = %s
            WHERE MaCV = %s
            """, (MaCV, TenCV, maCV))
        mysql.connection.commit()
        return redirect(url_for('table_chuc_vu'))
    
    if (mode == "E"):
        cur.execute("""
        SELECT *
        FROM qlnv_chucvu
        WHERE MaCV = %s""", (maCV, ))
        chucvu = cur.fetchall()
        
        if (len(chucvu) == 0):
            abort(404)
        
        return render_template(session['role'] +"chucvu/form_view_update_chuc_vu.html", 
                                edit_view = mode,
                                maCV = maCV,
                                chucvu = chucvu[0],
                                congty = session['congty'],
                                my_user = session['username'])
    cur.close()
    return render_template(session['role'] +"chucvu/form_view_update_chuc_vu.html",
                           chucvu = chucvu,
                           congty = session['congty'],
                           my_user = session['username'])
    
@login_required
@app.route("/form_add_chuc_vu", methods=['GET','POST'])
def form_add_chuc_vu():
    if session['role_id'] != 1:
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM qlnv_chucvu""")
    chucvu = cur.fetchall()
    
    if request.method == 'POST':
        details = request.form
        MaCV = details['MaCV'].strip()
        TenCV = details["TenCV"].strip()
        
        for data in chucvu:
            if (MaCV in data):
                return render_template(session['role'] +"form_add_chuc_vu.html", 
                                       congty = session['congty'],
                                       ma_err = "True",
                                       my_user = session['username'])
        
        cur.execute("INSERT INTO qlnv_chucvu(MaCV, TenCV) VALUES (%s, %s)",(MaCV, TenCV))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for("table_chuc_vu"))
    return render_template(session['role'] +"chucvu/form_add_chuc_vu.html",
                           congty=session['congty'],
                           my_user = session['username'])



@login_required
@app.route("/table_chuc_vu/<string:maCV>")
def table_chuc_vu_nhan_vien(maCV):
    if session['role_id'] != 1:
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT TenCV
        FROM qlnv_chucvu 
        WHERE MaCV = %s """, (maCV, ))
    tenCV = cur.fetchall()
    if (len(tenCV) != 1):
        abort(404)
    
    cur.execute("""
        SELECT nv.MaNhanVien, nv.TenNV,DATE_FORMAT(nv.NgaySinh,"%d-%m-%Y"), nv.DienThoai, cv.TenCV, DATE_FORMAT(tg.NgayNhanChuc,"%d-%m-%Y")
        FROM qlnv_chucvu cv
        JOIN qlnv_thoigiancongtac tg ON tg.MaCV = cv.MaCV
        JOIN qlnv_nhanvien nv ON tg.MaNV = nv.MaNhanVien
        WHERE cv.MaCV = '""" + str(maCV) + """' AND tg.DuongNhiem = 1 """)
    nv_chuc_vu = cur.fetchall()
    
    cur.close()
    return render_template(session['role'] +"chucvu/table_chuc_vu_nhan_vien.html",
                           tenCV = tenCV,
                           nv_chuc_vu=nv_chuc_vu,
                           maCV = maCV,
                           congty = session['congty'],
                           my_user = session['username'])


@login_required
@app.route("/delete_chuc_vu/<string:maCV>")
def delete_chuc_vu(maCV):
    if session['role_id'] != 1:
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT cv.MaCV, cv.TenCV, COUNT(nv.MaNhanVien) 
        FROM qlnv_chucvu cv
        LEFT JOIN qlnv_nhanvien nv ON cv.MaCV = nv.MaChucVu
        LEFT JOIN qlnv_thoigiancongtac tg ON tg.MaNV = nv.MaNhanVien 
        WHERE CV.MaCV = %s
        GROUP BY cv.MaCV""", (maCV, ))
    chucvu = cur.fetchall()
    
    # Check xem chức vụ này còn nhân viên nào không
    if chucvu[0][2] != 0:
        abort(404)
    
    sql = "DELETE FROM qlnv_chucvu WHERE MaCV=%s"
    val = (maCV, )
    cur.execute(sql,val)
    mysql.connection.commit()
    return redirect(url_for('table_chuc_vu'))
#
# ------------------ CHUC VU ------------------------
#

#
# ------------------ CHAM CONG ------------------------
#
@login_required
@app.route("/danh_sach_cham_cong", methods=['GET','POST'])
def danh_sach_cham_cong():
    cur = mysql.connection.cursor()
    
    mucPhanLoaiChamCong = [124,180]
    Nam = datetime.datetime.now().year
    
    if session['role_id'] != 1:
        cur.execute("""
                    SELECT * 
                    FROM qlnv_chamcongthang
                    WHERE Nam = %s AND MaNV = %s
                    """, (Nam, session['username'][4]))
    else:
        cur.execute("""
                    SELECT * 
                    FROM qlnv_chamcongthang
                    WHERE Nam = %s
                    """, (Nam, ))
    chamcongtheocacthang = cur.fetchall()
    
    if request.method == 'POST':
        detail = request.form
        Nam = int(detail['Year'].strip())
        if session['role_id'] != 1:
            cur.execute("""
                        SELECT * 
                        FROM qlnv_chamcongthang
                        WHERE Nam = %s AND MaNV = %s
                        """, (Nam, session['username'][4]))
        else:
            cur.execute("""
                        SELECT * 
                        FROM qlnv_chamcongthang
                        WHERE Nam = %s
                        """, (Nam, ))
        chamcongtheocacthang = cur.fetchall()
    
    cur.close()
    return render_template(session['role'] +'chamcong/bang_cham_cong_thang.html',
                           mucPhanLoaiChamCong = mucPhanLoaiChamCong,
                           Nam = Nam,
                           chamcongtheocacthang = chamcongtheocacthang,
                           congty = session['congty'],
                           my_user = session['username'])


@login_required
@app.route("/table_cham_cong_tong_ket_thang/<string:maNV>_<string:year>")
def table_cham_cong_tong_ket_thang(maNV,year):
    cur = mysql.connection.cursor()
    if session['role_id'] != 1:
        cur.execute("""
                    SELECT TenNV
                    FROM qlnv_nhanvien
                    WHERE MaNhanVien = %s
                    """, (session['username'][4],))
    else:
        cur.execute("""
                    SELECT TenNV
                    FROM qlnv_nhanvien
                    WHERE MaNhanVien = %s
                    """, (maNV,))
    tenNV = cur.fetchall()
    
    if (len(tenNV) == 0):
        abort(404)
    
    tenNV = tenNV[0][0]
    if session['role_id'] != 1:
        cur.execute("""
                    SELECT * 
                    FROM qlnv_chamcongtongketthang
                    WHERE MaNhanVien = %s AND Nam = %s 
                    ORDER BY Thang ASC
                    """, (session['username'][4], year))
    else:
        cur.execute("""
                    SELECT * 
                    FROM qlnv_chamcongtongketthang
                    WHERE MaNhanVien = %s AND Nam = %s 
                    ORDER BY Thang ASC
                    """, (maNV, year))
    data_tong_ket_thang = cur.fetchall()
    
    if (len(data_tong_ket_thang) == 0):
        abort(404)
    
    data_tong_ket_thang = data_tong_ket_thang
    
    return render_template(session['role'] +'chamcong/bang_cham_cong_thang_tong_ket.html',
                           TenNV = tenNV,
                           Nam = year,
                           MaNV = maNV,
                           data_tong_ket_thang = data_tong_ket_thang,
                           congty = session['congty'],
                           my_user = session['username'])

    
@login_required
@app.route("/table_cham_cong_ngay_trong_thang/<string:maNV>_<string:year>_<string:month>")
def table_cham_cong_ngay_trong_thang(maNV,year,month):
    sql = """
        SELECT * 
        FROM qlnv_chamcong cc 
        WHERE YEAR(cc.Ngay) = %s AND MONTH(cc.Ngay) = %s AND MaNV = %s
        ORDER BY cc.Ngay ASC, cc.GioVao ASC;
    """
    
    val = (year, month, maNV)
    if session['role_id'] != 1:
        sql = """
            SELECT * 
            FROM qlnv_chamcong cc 
            WHERE YEAR(cc.Ngay) = %s AND MONTH(cc.Ngay) = %s AND MaNV = %s
            ORDER BY cc.Ngay ASC, cc.GioVao ASC;
        """
        val = (year, month, session['username'][4])
        
    cur = mysql.connection.cursor()
    
    cur.execute(sql, val)
    chamcong = cur.fetchall()
    
    if (len(chamcong) == 0):
        abort(404)
    
    if session['role_id'] != 1:
        cur.execute("""
                    SELECT TenNV
                    FROM qlnv_nhanvien
                    WHERE MaNhanVien = %s
                    """, (session['username'][4],))
    else:
        cur.execute("""
                    SELECT TenNV
                    FROM qlnv_nhanvien
                    WHERE MaNhanVien = %s
                    """, (maNV,))
    tenNV = cur.fetchall()
    
    
    if (len(tenNV) == 0):
        abort(404)
    
    tenNV = tenNV[0][0]
    
    column_name = ['ID','MaNV','Ngay', 'GioVao','GioRa','OT','ThoiGianLamViec','ThoiGianFloat']
    data = pd.DataFrame.from_records(chamcong, columns=column_name)
    
    # data = data.set_index('ID')
    # pathFile = app.config['SAVE_FOLDER_EXCEL'] + "/" + "Data_ChamCong_" + maNV + "_" + month + "_" + year +".xlsx"
    # data.to_excel(pathFile)
    # return send_file(pathFile, as_attachment=True)
    
    data['ThoiGianLamViec']= (pd.to_timedelta(data['GioRa'].astype(str)) - 
                             pd.to_timedelta(data['GioVao'].astype(str)))
    data['ThoiGianLamViec'] = pd.to_numeric(data['ThoiGianLamViec']) / (3600 * 10**9) 
    
    index_arr = []
    index = 0
    date_arr = []
    id_arr = []
    time_arr = []
    for date in data.Ngay.unique():
        index_arr.append(index)
        tmp_id_list = []
        tmp_time_lst = []
        for elm in data[data['Ngay'] == date].iloc:
            tmp_id_list.append(elm['ID'])
            tmp_time_lst.append((elm['GioVao'], elm['GioRa']))
        time_arr.append(tmp_time_lst)
        id_arr.append(tmp_id_list)
        date_arr.append(date)
        index += 1
        
    dict_week_day = {
        0 : "Thứ hai",
        1 : "Thứ ba",
        2 : "Thứ tư",
        3 : "Thứ năm",
        4 : "Thứ sáu",
        5 : "Thứ bảy",
        6 : "Chủ nhật"
    }
    
    date_str = []
    date_weekday = []
    for elm in date_arr:
        date_weekday.append(dict_week_day[elm.weekday()])
        date_str.append(elm.strftime("%d-%m-%Y"))
    
    day = [int(elm[:2:]) for elm in date_str]
    
    time_arr_str = []
    for elm in time_arr:
        tmp_index_lst =[]
        for i in elm:
            tmp_lst = []
            for j in i:
                tmp_lst.append(str(j)[6::])
            tmp_index_lst.append(tmp_lst)
        time_arr_str.append(tmp_index_lst)
        
    # lấy data tổng kết ngày từ bảng qlnv_chamcongngay
    sql = "SELECT MaChamCong, MaNV, Nam, Thang, SoNgayThang,"
    for i in day:
        sql += "Ngay" + str(i) + ","
    sql = sql[:-1:]
    sql += " FROM qlnv_chamcongngay WHERE Thang = %s AND MaNV = %s AND Nam = %s"
    cur.execute(sql,(month, maNV, year))
    data_tong_ket = cur.fetchall()
    
    if (len(data_tong_ket) == 0):
        abort(404)
    data_tong_ket = data_tong_ket[0]
    data_day_tong_ket = [data_tong_ket[4 + i] for i in range(1,1+len(day))]
    cur.close()

    return render_template(session['role'] +'chamcong/bang_cham_cong_ngay.html',
                           TenNV = tenNV,
                           date_weekday = date_weekday,
                           month = month,
                           maNV = maNV,
                           year = year,
                           data_day_tong_ket = data_day_tong_ket,
                           day = day,
                           date_str = date_str,
                           time_arr_str = time_arr_str,
                           id_arr = id_arr,
                           index_arr = index_arr,
                           congty = session['congty'],
                           my_user = session['username'])

@login_required
@app.route("/graph_cham_cong_ngay/<string:maNV>_<string:year>_<string:month>")
def graph_cham_cong_ngay(maNV,year,month):
    cur = mysql.connection.cursor()
    
    cur.execute("""
                SELECT TenNV
                FROM qlnv_nhanvien
                WHERE MaNhanVien = %s
                """, (maNV,))
    tenNV = cur.fetchall()
    
    if (len(tenNV) == 0):
        abort(404)
    
    tenNV = tenNV[0][0]
    
    return render_template('chamcong/graph_cham_cong_ngay.html',
                           TenNV = tenNV,
                           month = month,
                           maNV = maNV,
                           year = year,
                           congty = session['congty'],
                           my_user = session['username'])
    
@login_required
@app.route("/get_plot_cham_cong_tong_ket_thang/<string:maNV>_<string:year>_<string:month>")
def get_plot_cham_cong_tong_ket_thang(maNV,year,month):
    sql = """
        SELECT * 
        FROM qlnv_chamcong cc 
        WHERE YEAR(cc.Ngay) = %s AND MONTH(cc.Ngay) = %s AND MaNV = %s
        ORDER BY cc.Ngay ASC, cc.GioVao ASC;
    """
    val = (year, month, maNV)
    
    cur = mysql.connection.cursor()
    
    cur.execute("""
                SELECT TenNV
                FROM qlnv_nhanvien
                WHERE MaNhanVien = %s
                """, (maNV,))
    tenNV = cur.fetchall()
    
    if (len(tenNV) == 0):
        abort(404)
    
    tenNV = tenNV[0][0]
    
    cur.execute(sql, val)
    chamcong = cur.fetchall()
    
    if (len(chamcong) == 0):
        abort(404)
    
    date_str = []
    date_start = datetime.datetime(int(year), int(month), 1)
    date_step = datetime.timedelta(days=1)
    while (int(date_start.month) == int(month)):
        date_str.append(date_start.strftime("%d-%m-%Y")) 
        date_start += date_step
        
    # lấy data tổng kết ngày từ bảng qlnv_chamcongngay
    sql = "SELECT *"
    sql += " FROM qlnv_chamcongngay WHERE Thang = %s AND MaNV = %s AND Nam = %s"
    cur.execute(sql,(month, maNV, year))
    data_tong_ket = cur.fetchall()
    
    if (len(data_tong_ket) == 0):
        abort(404)
    
    data_tong_ket = data_tong_ket[0]
    data_day_tong_ket = [data_tong_ket[4 + i] if data_tong_ket[4 + i] != -1 else 0 for i in range(1,data_tong_ket[4]+1)]
    cur.close()
    
    fig,axis=plt.subplots(figsize=(7,8))
    axis=sns.set(style="darkgrid")
    g = sns.lineplot(x= date_str, y =data_day_tong_ket)
    g.set_title("Biểu đồ cho nhân viên " + tenNV + " trong tháng " + month + " năm " + year)
    g.set_xlabel("Ngày")
    g.set_ylabel("Tổng số giờ làm trong ngày")
    g.set_xticklabels([int(elm[:2:]) for elm in date_str], rotation = (30), fontsize = 7)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
    

@login_required
@app.route('/form_view_update_cham_cong/<string:canEdit>_<string:maNV>_<string:id>_<string:day>_<string:month>_<string:year>', methods = ['GET','POST'])
def form_view_update_cham_cong(canEdit, maNV, id, day, month, year):
    if session['role_id'] != 1:
        abort(404)
    sql = """
        SELECT * 
        FROM qlnv_chamcong cc 
        WHERE YEAR(cc.Ngay) = %s AND MONTH(cc.Ngay) = %s AND DAY(cc.Ngay) = %s AND MaNV = %s
        ORDER BY cc.Ngay ASC, cc.GioVao ASC;
    """
    val = (year, month, day, maNV)
    
    cur = mysql.connection.cursor()
    
    cur.execute("""
                SELECT TenNV
                FROM qlnv_nhanvien
                WHERE MaNhanVien = %s
                """, (maNV,))
    tenNV = cur.fetchall()
    
    if (len(tenNV) == 0):
        abort(404)
    
    tenNV = tenNV[0][0]
    
    cur.execute(sql, val)
    chamcong = cur.fetchall()
    
    if (len(chamcong) == 0):
        abort(404)
    
    column_name = ['ID','MaNV','Ngay', 'GioVao','GioRa','OT','ThoiGianLamViec','ThoiGianFloat']
    data = pd.DataFrame.from_records(chamcong, columns=column_name)
    
    index_arr = []
    index = 0
    date_arr = []
    id_arr = []
    time_arr = []
    for date in data.Ngay.unique():
        for elm in data[data['Ngay'] == date].iloc:
            index_arr.append(index)
            id_arr.append(elm['ID'])
            time_arr.append((elm['GioVao'], elm['GioRa']))
            index += 1
        date_arr.append(date)
    
    date_arr = date_arr[0]
    
    dict_week_day = {
        0 : "Thứ hai",
        1 : "Thứ ba",
        2 : "Thứ tư",
        3 : "Thứ năm",
        4 : "Thứ sáu",
        5 : "Thứ bảy",
        6 : "Chủ nhật"
    }
    
    date_weekday = dict_week_day[date_arr.weekday()]
    date_str = date_arr.strftime("%d-%m-%Y")
    
    day = int(date_str[:2:])
    
    time_arr_str = []
    for elm in time_arr:
        tmp_lst = []
        for j in elm:
            tmp_lst.append(str(j)[6::])
        time_arr_str.append(tmp_lst)
    
    if request.method == 'POST':
        detail = request.form
        NGAY = datetime.datetime(int(year), int(month), int(day))
        GIOVAO = detail['GioVao']
        GIORA = detail['GioRa']
        OT = detail['OT']
        
        if (GIORA < GIOVAO):
            abort(404)
        
        sql = """
            SELECT ThoiGian_thap_phan
            FROM qlnv_chamcong
            WHERE id = %s
            """
        cur.execute(sql, (id, ))
        tg_ThapPhan_old = cur.fetchall()
        
        if (len(tg_ThapPhan_old) == 0):
            abort(404)
        
        tg_ThapPhan_old = tg_ThapPhan_old[0][0]
        
        sql_chamcong = """
            UPDATE `qlnv_chamcong` 
            SET GioVao = %s, GioRa = %s, OT = %s
            WHERE id = %s;
        """
        cur.execute(sql_chamcong, (GIOVAO, GIORA, OT, id))
        mysql.connection.commit()
        
        cur.execute("""
                    SELECT ThoiGian_thap_phan
                    FROM qlnv_chamcong
                    WHERE MaNV = %s AND Ngay=%s AND GioVao=%s AND GioRa=%s AND OT =%s
                    """, (maNV, NGAY.date(), GIOVAO, GIORA, OT))
        tg_ThapPhan_new = cur.fetchall()[0][0]
        
        if (OT == 1):
            tg_ThapPhan_new *= 2 # tang ca huong luong x2
            
        diff = tg_ThapPhan_new - tg_ThapPhan_old
        
        #check ton tai
        cur.execute("""SELECT MaChamCong, SoNgayThang, Ngay""" + str(NGAY.day) + """
                    FROM qlnv_chamcongngay
                    WHERE Nam = %s AND Thang = %s AND MaNV = %s""", (NGAY.year, NGAY.month,maNV) )
        chamCongTheoThang = cur.fetchall()
        
        # check ton tai nam
        cur.execute("""SELECT id, MaNV, T""" + str(NGAY.month) + """
                    FROM qlnv_chamcongthang
                    WHERE Nam = %s AND MaNV = %s""", (NGAY.year, maNV) )
        chamCongTheoNam = cur.fetchall()
        
        # Xử lý trong bảng chấm công ngày và trong bảng tổng hợp theo các năm
        if (len(chamCongTheoThang) == 0 or len(chamCongTheoNam) == 0):
            abort(404)
        else:
            chamCongTheoThang = chamCongTheoThang[0]
            sql_chamcongngay = "UPDATE qlnv_chamcongngay SET "
            if chamCongTheoThang[2] == -1:
                abort(404)
            else:
                sql_chamcongngay += "Ngay" + str(NGAY.day) + " = Ngay" + str(NGAY.day) + "+ '" + str(diff) + "'" 
            sql_chamcongngay += " WHERE MaNV = '" + maNV  + "' AND Nam = '" + str(NGAY.year) + "' AND Thang = '" + str(NGAY.month) + "'"
            cur.execute(sql_chamcongngay)
            mysql.connection.commit()
                    
            chamCongTheoNam = chamCongTheoNam[0]
            sql_chamcongthang = "UPDATE qlnv_chamcongthang SET "
            if chamCongTheoNam[2] == -1:
                abort(404)
            else:
                sql_chamcongthang += "T" + str(NGAY.month) + " = T" + str(NGAY.month) + "+ '" + str(diff) + "'" 
            sql_chamcongthang += " WHERE MaNV = '" + maNV  + "' AND Nam = '" + str(NGAY.year) + "'"
            cur.execute(sql_chamcongthang)
            mysql.connection.commit()
        
        # Xử lý trong bảng tổng kết tháng    
        cur.execute("""SELECT *
                    FROM qlnv_chamcongtongketthang
                    WHERE Nam = %s AND Thang = %s AND MaNhanVien = %s""", (NGAY.year, NGAY.month,maNV) )
        chamCongTongKet = cur.fetchall()
        
        day_to_count = calendar.SUNDAY

        matrix = calendar.monthcalendar(NGAY.year,NGAY.month)

        num_sun_days = sum(1 for x in matrix if x[day_to_count] != 0)
        
        if (len(chamCongTongKet) == 0):
            soNgayDiLam = 1
            soNgayDiVang = monthrange(NGAY.year, NGAY.month)[1] - 1 - num_sun_days
            soNgayTangCa = 0
            if OT == 1:
                soNgayTangCa = 1
            tongSoNgay = 1
            cur.execute("""INSERT INTO `qlnv_chamcongtongketthang` (`Id`, `MaNhanVien`, `Nam`, `Thang`,
                        `SoNgayDiLam`, `SoNgayDiVang`, `SoNgayTangCa`, `TongSoNgay`)
                        VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)""", (maNV, NGAY.year, NGAY.month, soNgayDiLam,
                                                                       soNgayDiVang, soNgayTangCa, tongSoNgay))
            mysql.connection.commit()
        else:
            cur.execute("""
                        SELECT COUNT(DISTINCT Ngay)
                        FROM qlnv_chamcong
                        WHERE MaNV = %s AND Month(Ngay)=%s AND YEAR(Ngay)=%s
                        GROUP BY Month(Ngay)
                        """, (maNV, NGAY.month, NGAY.year))
            soNgayDiLam = cur.fetchall()[0][0]
            soNgayDiVang = monthrange(NGAY.year, NGAY.month)[1] - soNgayDiLam - num_sun_days
            cur.execute("""
                        SELECT COUNT(DISTINCT Ngay)
                        FROM qlnv_chamcong
                        WHERE MaNV = %s AND Month(Ngay)=%s AND YEAR(Ngay)=%s AND OT = 1
                        GROUP BY Month(Ngay)
                        """, (maNV, NGAY.month, NGAY.year))
            soNgayTangCa = cur.fetchall()
            if (len(soNgayTangCa) == 0):
                soNgayTangCa = 0
            else:
                soNgayTangCa = soNgayTangCa[0][0]
            tongSoNgay = soNgayDiLam
            cur.execute("""UPDATE qlnv_chamcongtongketthang
                        SET SoNgayDiLam = %s, SoNgayDiVang = %s, SoNgayTangCa=%s, TongSoNgay = %s
                        WHERE MaNhanVien = %s AND Nam = %s AND Thang = %s""", (soNgayDiLam, soNgayDiVang, soNgayTangCa,
                                                                               tongSoNgay, maNV, NGAY.year, NGAY.month))
            mysql.connection.commit()
        
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('table_cham_cong_ngay_trong_thang', maNV = maNV, year = year, month = month))
    
    if canEdit == 'E':
        sql = """
            SELECT * 
            FROM qlnv_chamcong cc 
            WHERE id = %s
            ORDER BY cc.Ngay ASC, cc.GioVao ASC;
        """
        cur.execute(sql, (id, ))
        
        chamcong = cur.fetchall()
        
        if (len(chamcong) == 0):
            abort(404)
        
        chamcong = chamcong[0]
        
        # format data
        new_chamcong = list(chamcong[0:3:])
        if len(str(chamcong[3])) != 8:
            new_chamcong.append("0" + str(chamcong[3]))
        else:
            new_chamcong.append(str(chamcong[3]))
            
        if len(str(chamcong[4])) != 8:
            new_chamcong.append("0" + str(chamcong[4]))
        else:
            new_chamcong.append(str(chamcong[4]))
        new_chamcong.append(chamcong[5])
        
        return render_template(session['role'] +"chamcong/form_view_update_cham_cong.html",
                           TenNV = tenNV,
                           edit = 'E',
                           chamcong = new_chamcong,
                           MaNV = maNV,
                           day = day,
                           month = month,
                           year = year,
                           date_weekday = date_weekday,
                           date_str = date_str,
                           congty = session['congty'],
                           my_user = session['username'])
    
    cur.close()
    return render_template(session['role'] +"chamcong/form_view_update_cham_cong.html",
                           TenNV = tenNV,
                           chamcong = chamcong,
                           index_arr = index_arr,
                           time_arr_str = time_arr_str,
                           MaNV = maNV,
                           id_arr = id_arr,
                           day = day,
                           month = month,
                           year = year,
                           date_weekday = date_weekday,
                           date_str = date_str,
                           congty = session['congty'],
                           my_user = session['username'])
        
@login_required
@app.route('/delete_cham_cong/<string:id>')
def delete_cham_cong(id):
    if session['role_id'] != 1:
        abort(404)
    sql = """
        SELECT * 
        FROM qlnv_chamcong
        WHERE id = %s
    """
    cur = mysql.connection.cursor()
    
    cur.execute(sql, (id, ))
    old_chamcong = cur.fetchall()
    
    if (len(old_chamcong) == 0):
        return "Error 1"
    
    old_chamcong = old_chamcong[0]
    maNV = old_chamcong[1]
    NGAY = old_chamcong[2]
    tg_ThapPhan = old_chamcong[7]
    
    sql = """
        DELETE FROM qlnv_chamcong WHERE id = %s
    """
    cur.execute(sql, (id, ))
    mysql.connection.commit()
    
    #check ton tai
    cur.execute("""SELECT MaChamCong, SoNgayThang, Ngay""" + str(NGAY.day) + """
                FROM qlnv_chamcongngay
                WHERE Nam = %s AND Thang = %s AND MaNV = %s""", (NGAY.year, NGAY.month,maNV) )
    chamCongTheoThang = cur.fetchall()
    
    # check ton tai nam
    cur.execute("""SELECT id, MaNV, T""" + str(NGAY.month) + """
                FROM qlnv_chamcongthang
                WHERE Nam = %s AND MaNV = %s""", (NGAY.year, maNV) )
    chamCongTheoNam = cur.fetchall()
    
    # Xử lý trong bảng chấm công ngày và trong bảng tổng hợp theo các năm
    if (len(chamCongTheoThang) == 0 or len(chamCongTheoNam) == 0):
        return "Error 2"
    else:
        chamCongTheoThang = chamCongTheoThang[0]
        sql_chamcongngay = "UPDATE qlnv_chamcongngay SET "
        if chamCongTheoThang[2] == -1:
            return "Error 3"
        else:
            sql_chamcongngay += "Ngay" + str(NGAY.day) + " = Ngay" + str(NGAY.day) + "- '" + str(tg_ThapPhan) + "'" 
        sql_chamcongngay += " WHERE MaNV = '" + maNV  + "' AND Nam = '" + str(NGAY.year) + "' AND Thang = '" + str(NGAY.month) + "'"
        cur.execute(sql_chamcongngay)
        mysql.connection.commit()
        
        #check xem có trống bản ghi với ngày trong tháng đó không
        cur.execute("""SELECT MaChamCong, SoNgayThang, Ngay""" + str(NGAY.day) + """
                FROM qlnv_chamcongngay
                WHERE Nam = %s AND Thang = %s AND MaNV = %s""", (NGAY.year, NGAY.month,maNV) )
        chamCongTheoThang = cur.fetchall()[0]
        if (chamCongTheoThang[2] == 0):
            sql_chamcongngay = "UPDATE qlnv_chamcongngay SET "
            sql_chamcongngay += "Ngay" + str(NGAY.day) + " = " + "'" + str(-1) + "'"
            sql_chamcongngay += " WHERE MaNV = '" + maNV  + "' AND Nam = '" + str(NGAY.year) + "' AND Thang = '" + str(NGAY.month) + "'"
            cur.execute(sql_chamcongngay) 
            mysql.connection.commit()
        
        cur.execute("""SELECT *
                FROM qlnv_chamcongngay
                WHERE Nam = %s AND Thang = %s AND MaNV = %s""", (NGAY.year, NGAY.month,maNV) )
        chamCongTheoThang = cur.fetchall()[0]
        check_del = True
        for elm in chamCongTheoThang[5:36]:
            if (elm != -1):
                check_del = False
                break
        if (check_del):
            sql_chamcongngay = "DELETE FROM qlnv_chamcongngay "
            sql_chamcongngay += " WHERE MaNV = '" + maNV  + "' AND Nam = '" + str(NGAY.year) + "' AND Thang = '" + str(NGAY.month) + "'"
            cur.execute(sql_chamcongngay) 
            mysql.connection.commit()
        
        chamCongTheoNam = chamCongTheoNam[0]
        sql_chamcongthang = "UPDATE qlnv_chamcongthang SET "
        if chamCongTheoNam[2] == -1:
            return "Error 4"
        else:
            sql_chamcongthang += "T" + str(NGAY.month) + " = T" + str(NGAY.month) + "- '" + str(tg_ThapPhan) + "'" 
        sql_chamcongthang += " WHERE MaNV = '" + maNV  + "' AND Nam = '" + str(NGAY.year) + "'"
        cur.execute(sql_chamcongthang)
        mysql.connection.commit()
        
        
        # check xem xem có trống bản ghi trong năm đó không
        cur.execute("""SELECT id, MaNV, T""" + str(NGAY.month) + """
                    FROM qlnv_chamcongthang
                    WHERE Nam = %s AND MaNV = %s""", (NGAY.year, maNV) )
        chamCongTheoNam = cur.fetchall()
        chamCongTheoNam = chamCongTheoNam[0]
        if (chamCongTheoNam[2] == 0):
            sql_chamcongthang = "UPDATE qlnv_chamcongthang SET "
            sql_chamcongthang += "T" + str(NGAY.month) + " = " + " '" + str(-1) + "'" 
            sql_chamcongthang += " WHERE MaNV = '" + maNV  + "' AND Nam = '" + str(NGAY.year) + "'"
            cur.execute(sql_chamcongthang)
            mysql.connection.commit()
        
        cur.execute("""SELECT *
                    FROM qlnv_chamcongthang
                    WHERE Nam = %s AND MaNV = %s""", (NGAY.year, maNV) )
        chamCongTheoNam = cur.fetchall()[0]
        check_del = True
        for elm in chamCongTheoNam[3:15]:
            if (elm != -1):
                check_del = False
                break
        if (check_del):
            sql_chamcongthang = "DELETE FROM qlnv_chamcongthang "
            sql_chamcongthang += " WHERE MaNV = '" + maNV  + "' AND Nam = '" + str(NGAY.year) + "'"
            cur.execute(sql_chamcongthang)
            mysql.connection.commit()
            
        
    # Xử lý trong bảng tổng kết tháng    
    cur.execute("""SELECT *
                FROM qlnv_chamcongtongketthang
                WHERE Nam = %s AND Thang = %s AND MaNhanVien = %s""", (NGAY.year, NGAY.month,maNV) )
    chamCongTongKet = cur.fetchall()
    
    day_to_count = calendar.SUNDAY
    matrix = calendar.monthcalendar(NGAY.year,NGAY.month)
    num_sun_days = sum(1 for x in matrix if x[day_to_count] != 0)
    
    if (len(chamCongTongKet) == 0):
        return "Error 5"
    else:
        cur.execute("""
                    SELECT COUNT(DISTINCT Ngay)
                    FROM qlnv_chamcong
                    WHERE MaNV = %s AND Month(Ngay)=%s AND YEAR(Ngay)=%s
                    GROUP BY Month(Ngay)
                    """, (maNV, NGAY.month, NGAY.year))
        soNgayDiLam = cur.fetchall()
        if (len(soNgayDiLam) == 0):
            cur.execute("""
                        DELETE FROM qlnv_chamcongtongketthang
                        WHERE MaNhanVien = %s AND Nam = %s AND Thang = %s""",
                        (maNV, NGAY.year, NGAY.month))
            mysql.connection.commit()
            return redirect(url_for('table_cham_cong_ngay_trong_thang', maNV = maNV, year = NGAY.year, month = NGAY.month))
        else:
            soNgayDiLam = soNgayDiLam[0][0]
        soNgayDiVang = monthrange(NGAY.year, NGAY.month)[1] - soNgayDiLam - num_sun_days
        cur.execute("""
                    SELECT COUNT(DISTINCT Ngay)
                    FROM qlnv_chamcong
                    WHERE MaNV = %s AND Month(Ngay)=%s AND YEAR(Ngay)=%s AND OT = 1
                    GROUP BY Month(Ngay)
                    """, (maNV, NGAY.month, NGAY.year))
        soNgayTangCa = cur.fetchall()
        if (len(soNgayTangCa) == 0):
            soNgayTangCa = 0
        else:
            soNgayTangCa = soNgayTangCa[0][0]
        tongSoNgay = soNgayDiLam
        cur.execute("""UPDATE qlnv_chamcongtongketthang
                    SET SoNgayDiLam = %s, SoNgayDiVang = %s, SoNgayTangCa=%s, TongSoNgay = %s
                    WHERE MaNhanVien = %s AND Nam = %s AND Thang = %s""", (soNgayDiLam, soNgayDiVang, soNgayTangCa,
                                                                            tongSoNgay, maNV, NGAY.year, NGAY.month))
        mysql.connection.commit()
    cur.close()
    return redirect(url_for('danh_sach_cham_cong'))
    
@login_required
@app.route('/form_add_data_cham_cong', methods=['GET','POST'])
def form_add_data_cham_cong():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        if (session['role_id'] == 1):
            detail = request.form
            NGAY = datetime.datetime.strptime(detail['Ngay'].strip(), '%Y-%m-%d')
            MANV = detail['MANV']
            GIOVAO = detail['GioVao']
            GIORA = detail['GioRa']
            OT = detail['OT']
        else:
            if 'chamcong' not in session.keys():
                NGAY = datetime.datetime.now().strftime('%Y-%m-%d')
                MANV = session['username'][4]
                GIOVAO = datetime.datetime.now().strftime("%H:%M:%S")
                # GIORA = detail['GioRa']
                OT = 0
                data_in_session = (NGAY, MANV, GIOVAO, OT)
                session['chamcong'] = data_in_session
                return render_template(session['role'] +"chamcong/form_add_cham_cong.html",
                            chamcong = data_in_session,
                               is_chamcong = 'YES',
                           congty = session['congty'],
                           my_user = session['username'])
            else:
                NGAY = datetime.datetime.strptime(session['chamcong'][0], '%Y-%m-%d')
                MANV = session['username'][4]
                GIOVAO = session['chamcong'][2]
                GIORA = datetime.datetime.now().strftime("%H:%M:%S")
                OT = 0
                session.pop('chamcong')
        sql_chamcong = """
            INSERT INTO `qlnv_chamcong` (`id`, `MaNV`, `Ngay`, `GioVao`, `GioRa`, `OT`, `ThoiGianLamViec`, `ThoiGian_thap_phan`) 
            VALUES (NULL, %s, %s, %s, %s, %s, '', '0');
        """
        cur.execute(sql_chamcong, (MANV, NGAY.date(), GIOVAO, GIORA, OT))
        mysql.connection.commit()
        
        
        cur.execute("""
                    SELECT ThoiGian_thap_phan
                    FROM qlnv_chamcong
                    WHERE MaNV = %s AND Ngay=%s AND GioVao=%s AND GioRa=%s AND OT =%s
                    """, (MANV, NGAY.date(), GIOVAO, GIORA, OT))
        tg_ThapPhan = cur.fetchall()[0][0]
        
        if (OT == 1):
            tg_ThapPhan *= 2 # tang ca huong luong x2
        
        #check ton tai
        cur.execute("""SELECT MaChamCong, SoNgayThang, Ngay""" + str(NGAY.day) + """
                    FROM qlnv_chamcongngay
                    WHERE Nam = %s AND Thang = %s AND MaNV = %s""", (NGAY.year, NGAY.month,MANV) )
        chamCongTheoThang = cur.fetchall()
        
        # check ton tai nam
        cur.execute("""SELECT id, MaNV, T""" + str(NGAY.month) + """
                    FROM qlnv_chamcongthang
                    WHERE Nam = %s AND MaNV = %s""", (NGAY.year, MANV) )
        chamCongTheoNam = cur.fetchall()
        
        # Xử lý trong bảng chấm công ngày và trong bảng tổng hợp theo các năm
        if (len(chamCongTheoThang) == 0 or len(chamCongTheoNam) == 0):
            if len(chamCongTheoThang) == 0:
                cur.execute("""INSERT INTO `qlnv_chamcongngay` (`MaChamCong`, `MaNV`, `Nam`, `Thang`, `SoNgayThang`) VALUES
                        (NULL, %s, %s, %s, %s)""", (MANV, NGAY.year, NGAY.month, monthrange(NGAY.year, NGAY.month)[1]))
                 
            if len(chamCongTheoNam) == 0:
                cur.execute("""INSERT INTO qlnv_chamcongthang (id, MaNV, Nam) VALUES
                        (NULL, %s, %s)""", (MANV, NGAY.year))
            mysql.connection.commit()
            
            sql_chamcongngay = "UPDATE qlnv_chamcongngay SET "
            sql_chamcongngay += "Ngay" + str(NGAY.day) + " = '" + str(tg_ThapPhan) + "' "
            sql_chamcongngay += " WHERE MaNV = '" + MANV  + "' AND Nam = '" + str(NGAY.year) + "' AND Thang = '" + str(NGAY.month) + "'"
            cur.execute(sql_chamcongngay)
            mysql.connection.commit()
            
            sql_chamcongthang = "UPDATE qlnv_chamcongthang SET "
            sql_chamcongthang += "T" + str(NGAY.month) + " = '" + str(tg_ThapPhan) + "' "
            sql_chamcongthang += " WHERE MaNV = '" + MANV  + "' AND Nam = '" + str(NGAY.year) + "'"
            cur.execute(sql_chamcongthang)
            mysql.connection.commit()
        else:
            chamCongTheoThang = chamCongTheoThang[0]
            sql_chamcongngay = "UPDATE qlnv_chamcongngay SET "
            if chamCongTheoThang[2] == -1:
                sql_chamcongngay += "Ngay" + str(NGAY.day) + " = '" + str(tg_ThapPhan) + "' " 
            else:
                sql_chamcongngay += "Ngay" + str(NGAY.day) + " = Ngay" + str(NGAY.day) + "+ '" + str(tg_ThapPhan) + "'" 
            sql_chamcongngay += " WHERE MaNV = '" + MANV  + "' AND Nam = '" + str(NGAY.year) + "' AND Thang = '" + str(NGAY.month) + "'"
            cur.execute(sql_chamcongngay)
            mysql.connection.commit()
                    
            chamCongTheoNam = chamCongTheoNam[0]
            sql_chamcongthang = "UPDATE qlnv_chamcongthang SET "
            if chamCongTheoNam[2] == -1:
                sql_chamcongthang += "T" + str(NGAY.month) + " = '" + str(tg_ThapPhan) + "' " 
            else:
                sql_chamcongthang += "T" + str(NGAY.month) + " = T" + str(NGAY.month) + "+ '" + str(tg_ThapPhan) + "'" 
            sql_chamcongthang += " WHERE MaNV = '" + MANV  + "' AND Nam = '" + str(NGAY.year) + "'"
            cur.execute(sql_chamcongthang)
            mysql.connection.commit()
            
        # Xử lý trong bảng tổng kết tháng    
        cur.execute("""SELECT *
                    FROM qlnv_chamcongtongketthang
                    WHERE Nam = %s AND Thang = %s AND MaNhanVien = %s""", (NGAY.year, NGAY.month,MANV) )
        chamCongTongKet = cur.fetchall()
        
        day_to_count = calendar.SUNDAY

        matrix = calendar.monthcalendar(NGAY.year,NGAY.month)

        num_sun_days = sum(1 for x in matrix if x[day_to_count] != 0)
        
        if (len(chamCongTongKet) == 0):
            soNgayDiLam = 1
            soNgayDiVang = monthrange(NGAY.year, NGAY.month)[1] - 1 - num_sun_days
            soNgayTangCa = 0
            if OT == 1:
                soNgayTangCa = 1
            tongSoNgay = 1
            cur.execute("""INSERT INTO `qlnv_chamcongtongketthang` (`Id`, `MaNhanVien`, `Nam`, `Thang`,
                        `SoNgayDiLam`, `SoNgayDiVang`, `SoNgayTangCa`, `TongSoNgay`)
                        VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)""", (MANV, NGAY.year, NGAY.month, soNgayDiLam,
                                                                       soNgayDiVang, soNgayTangCa, tongSoNgay))
            mysql.connection.commit()
        else:
            cur.execute("""
                        SELECT COUNT(DISTINCT Ngay)
                        FROM qlnv_chamcong
                        WHERE MaNV = %s AND Month(Ngay)=%s AND YEAR(Ngay)=%s
                        GROUP BY Month(Ngay)
                        """, (MANV, NGAY.month, NGAY.year))
            soNgayDiLam = cur.fetchall()[0][0]
            soNgayDiVang = monthrange(NGAY.year, NGAY.month)[1] - soNgayDiLam - num_sun_days
            cur.execute("""
                        SELECT COUNT(DISTINCT Ngay)
                        FROM qlnv_chamcong
                        WHERE MaNV = %s AND Month(Ngay)=%s AND YEAR(Ngay)=%s AND OT = 1
                        GROUP BY Month(Ngay)
                        """, (MANV, NGAY.month, NGAY.year))
            soNgayTangCa = cur.fetchall()
            if (len(soNgayTangCa) == 0):
                soNgayTangCa = 0
            else:
                soNgayTangCa = soNgayTangCa[0][0]
            tongSoNgay = soNgayDiLam
            cur.execute("""UPDATE qlnv_chamcongtongketthang
                        SET SoNgayDiLam = %s, SoNgayDiVang = %s, SoNgayTangCa=%s, TongSoNgay = %s
                        WHERE MaNhanVien = %s AND Nam = %s AND Thang = %s""", (soNgayDiLam, soNgayDiVang, soNgayTangCa,
                                                                               tongSoNgay, MANV, NGAY.year, NGAY.month))
            mysql.connection.commit()
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('danh_sach_cham_cong'))
    
    if 'chamcong' in session:
        return render_template(session['role'] +"chamcong/form_add_cham_cong.html",
                               chamcong = session['chamcong'],
                               is_chamcong = 'YES',
                           congty = session['congty'],
                           my_user = session['username'])
    
    return render_template(session['role'] +"chamcong/form_add_cham_cong.html",
                           congty = session['congty'],
                           my_user = session['username'])


#
# ------------------ CHAM CONG ------------------------
#

# --Deivy--
# ------------------ PHONG BAN ------------------------
#

@login_required
@app.route('/view_all_phong_ban')
def view_all_phong_ban():
    if session['role_id'] == 3:
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute("""SELECT *
                FROM qlnv_phongban
                ORDER BY MaPB ASC""")
    raw_data = cur.fetchall()
    
    if (len(raw_data) == 0):
        abort(404)
    
    cur.execute("""SELECT COUNT(nv.MaNhanVien)
                FROM qlnv_nhanvien nv
                RIGHT JOIN qlnv_phongban pb ON nv.MaPhongBan = pb.MaPB
                GROUP BY MaPB
                ORDER BY MaPB ASC
                """)
    count_data = cur.fetchall()
    
    phongban = []
    for i in range(len(raw_data)):
        tmp_lst = []
        for elm in raw_data[i]:
            tmp_lst.append(elm)
        tmp_lst.append(count_data[i][0]) 
        # tmp_lst.append(count_data[i][0] if i < len(count_data) else 0) //sửa lỗi khi một phòng ban không có nhân viên
        phongban.append(tmp_lst)
    
    return render_template(session['role'] +"phongban/view_all_phong_ban.html",
                           phongban = phongban,
                           congty = session['congty'],
                           my_user = session['username'])
        
@login_required
@app.route('/view_phong_ban/<string:maPB>')
def view_phong_ban(maPB):
    if session['role_id'] == 3:
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute("""SELECT *
                FROM qlnv_phongban
                WHERE MaPB = %s
                ORDER BY MaPB ASC""", (maPB, ))
    raw_data = cur.fetchall()
    
    if (len(raw_data) == 0):
        abort(404)
    
    cur.execute("""SELECT COUNT(nv.MaNhanVien)
                FROM qlnv_nhanvien nv
                RIGHT JOIN qlnv_phongban pb ON nv.MaPhongBan = pb.MaPB
                WHERE MaPB = %s
                GROUP BY MaPB
                ORDER BY MaPB ASC
                """, (maPB, ))
    count_data = cur.fetchall()[0]
    # count_data = cur.fetchone()
    # phongban.append(count_data[0] if count_data else 0)
    
    cur.execute("""SELECT nv.MaNhanVien, nv.TenNV, img.PathToImage, nv.DiaChi, DATE_FORMAT(nv.NgaySinh,"%d-%m-%Y"), nv.GioiTinh, nv.DienThoai, cv.TenCV
                FROM qlnv_nhanvien nv
                RIGHT JOIN qlnv_phongban pb ON nv.MaPhongBan = pb.MaPB
                JOIN qlnv_chucvu cv ON nv.MaChucVu = cv.MaCV
                JOIN qlnv_imagedata img ON nv.ID_profile_image = img.ID_image
                WHERE MaPB = \"""" + maPB +"\"")
    nhanvien = cur.fetchall()
    
    phongban = []
    for elm in raw_data[0]:
        phongban.append(elm)
    phongban.append(count_data[0])
    
    cur.execute("""
                SELECT nv.TenNV, nv.DienThoai
                FROM qlnv_nhanvien nv
                WHERE nv.MaNhanVien = %s
                """, (phongban[4], ))
    # truongphong = cur.fetchall()[0]
    truongphong=cur.fetchone() 
    if not truongphong:
        truongphong = ("chưa có", "trống")
    
    cur.execute("""
                SELECT COUNT(*)
                FROM qlnv_thuongphat tp
                JOIN qlnv_nhanvien nv ON tp.MaNV = nv.MaNhanVien
                WHERE nv.MaPhongBan = %s
                AND tp.Loai = 1
                ORDER BY tp.Ngay DESC
                """, (maPB, ))
    num_phat = cur.fetchall()[0][0]
    
    cur.execute("""
                SELECT COUNT(*)
                FROM qlnv_thuongphat tp
                JOIN qlnv_nhanvien nv ON tp.MaNV = nv.MaNhanVien
                WHERE nv.MaPhongBan = %s
                AND tp.Loai = 0
                ORDER BY tp.Ngay DESC
                """, (maPB, ))
    num_thuong = cur.fetchall()[0][0]
    
    return render_template(session['role'] +'phongban/view_phong_ban.html',
                           num_thuong = num_thuong,
                           num_phat = num_phat,
                           truongphong = truongphong,
                           nhanvien = nhanvien,
                           phongban = phongban,
                           congty = session['congty'],
                           my_user = session['username'])

@login_required
@app.route('/form_update_phong_ban/<string:maPB>', methods=['GET', 'POST'])
def form_update_phong_ban(maPB):
    if session['role_id'] != 1:
        abort(404)
    cur = mysql.connection.cursor()
    
    cur.execute("""
                SELECT * FROM qlnv_phongban
                WHERE MaPB = %s
                """, (maPB, ))
    phongban = cur.fetchall()
    
    if (len(phongban) == 0):
        abort(404)
    
    phongban = phongban[0]
    
    if request.method == 'POST':
        detail = request.form
        MaPB = maPB
        TenPB = detail['TenPB']
        SDT = detail['SDT']
        MaTP = detail['MaTP']
        DIACHI = detail['DIACHI']
        
        if MaTP != phongban[4]:
            cur.execute("""
                        SELECT * 
                        FROM qlnv_nhanvien
                        WHERE MaNhanVien = %s 
                        """, (MaTP, ))

            if (len(cur.fetchall()) != 1):
                return render_template(session['role'] +'phongban/form_add_data_phong_ban.html',
                                    err = "Không tồn lại mã nhân viên " + MaTP,
                                    phongban = phongban,
                            congty = session['congty'],
                            my_user = session['username'])
        
            cur.execute("""
                        SELECT * 
                        FROM qlnv_phongban
                        WHERE MaTruongPhong = %s 
                        """, (MaTP, ))
            
            if (len(cur.fetchall()) != 0):
                return render_template(session['role'] +'phongban/form_add_data_phong_ban.html',
                                    phongban = phongban,
                                    err = "Nhân viên " + MaTP + " đã làm trưởng phòng phòng khác",
                            congty = session['congty'],
                            my_user = session['username'])
            
        cur.execute("""
                    UPDATE `qlnv_phongban`
                    SET `TenPB` = %s, `diachi` = %s, `sodt`=%s, `MaTruongPhong`=%s 
                    WHERE MaPB = %s;
                    """, ( TenPB, DIACHI, SDT, MaTP,MaPB))
        mysql.connection.commit()
        return redirect(url_for('view_all_phong_ban'))
    
    return render_template(session['role'] +'phongban/form_update_phong_ban.html',
                           phongban = phongban,
                           congty = session['congty'],
                           my_user = session['username'])

@login_required
@app.route('/delete_phong_ban/<string:maPB>')
def delete_phong_ban(maPB):
    if session['role_id'] != 1:
        abort(404)
    cur = mysql.connection.cursor()

    cur.execute("""
                SELECT COUNT(*)
                FROM qlnv_nhanvien
                WHERE MaPhongBan = %s
                """, (maPB, ))

    if (cur.fetchall()[0][0] != 0):
        abort(404)
    
    cur.execute("""
                DELETE FROM qlnv_phongban
                WHERE MaPB = %s
                """, (maPB, ))
    mysql.connection.commit()
    return redirect(url_for('view_all_phong_ban'))
    
@login_required
@app.route('/form_add_data_phong_ban', methods=['GET','POST'])
def form_add_data_phong_ban():
    if session['role_id'] != 1:
        abort(404)
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        detail = request.form
        MaPB = detail['MaPB']
        TenPB = detail['TenPB']
        SDT = detail['SDT']
        MaTP = detail['MaTP']
        DIACHI = detail['DIACHI']
        
        cur.execute("""
                    SELECT * 
                    FROM qlnv_nhanvien
                    WHERE MaNhanVien = %s 
                    """, (MaTP, ))

        if (len(cur.fetchall()) != 1):
            return render_template(session['role'] +'phongban/form_add_data_phong_ban.html',
                                   err = "Không tồn lại mã nhân viên " + MaTP,
                           congty = session['congty'],
                           my_user = session['username'])
        
        cur.execute("""
                    SELECT * 
                    FROM qlnv_phongban
                    WHERE MaTruongPhong = %s 
                    """, (MaTP, ))
        
        if (len(cur.fetchall()) != 0):
            return render_template(session['role'] +'phongban/form_add_data_phong_ban.html',
                                   err = "Nhân viên " + MaTP + " đã làm trưởng phòng phòng khác",
                           congty = session['congty'],
                           my_user = session['username'])
            
        cur.execute("""
                    SELECT * 
                    FROM qlnv_phongban
                    WHERE MaPB = %s 
                    """, (MaPB, ))
        
        if (len(cur.fetchall()) != 0):
            return render_template(session['role'] +'phongban/form_add_data_phong_ban.html',
                                   err = "Mã " + MaPB + " đã tồn tại",
                           congty = session['congty'],
                           my_user = session['username'])
        cur.execute("""
                    INSERT INTO `qlnv_phongban` (`MaPB`, `TenPB`, `diachi`, `sodt`, `MaTruongPhong`) 
                    VALUES (%s, %s, %s, %s, %s);
                    """, (MaPB, TenPB, DIACHI, SDT, MaTP))
        mysql.connection.commit()
        return redirect(url_for('view_all_phong_ban'))
    return render_template(session['role'] +'phongban/form_add_data_phong_ban.html',
                           congty = session['congty'],
                           my_user = session['username'])

@login_required
@app.route('/form_add_thuong_phat_phong_ban/<string:maPB>', methods=['GET','POST'])
def form_add_thuong_phat_phong_ban(maPB):
    if session['role_id'] == 3:
        abort(404)
    cur = mysql.connection.cursor()
    
    dct_type = {
        'Thưởng':0,
        'Kỷ luật':1
    }
    
    if request.method == 'POST':
        detail = request.form
        MaNV = detail['MaNV']
        LyDo = detail['LyDo']
        Loai = dct_type[detail['Loai']]
        Tien = detail['Tien']
        Ngay = detail['Ngay']
        GhiChu = detail['GhiChu']
        
        cur.execute("""
                    SELECT * 
                    FROM qlnv_nhanvien
                    WHERE MaNhanVien = %s AND MaPhongBan = %s
                    """, (MaNV, maPB))

        if (len(cur.fetchall()) != 1):
            return render_template(session['role'] +'phongban/form_add_thuong_phat_phong_ban.html',
                                   err = "Không tồn lại mã nhân viên " + MaNV + " ở phòng ban này",
                                   maPB = maPB,
                                    type = list(dct_type.keys()),
                           congty = session['congty'],
                           my_user = session['username'])
            
        cur.execute("""
                    INSERT INTO `qlnv_thuongphat` (`id`, `MaNV`, `Loai`, `LyDo`, `Tien`, `Ngay`, `GhiChu`)
                    VALUES (NULL, %s, %s, %s, %s, %s, %s);
                    """, (MaNV, Loai, LyDo, Tien, Ngay, GhiChu ))
        mysql.connection.commit()
        return redirect(url_for('view_phong_ban', maPB = maPB))
    
    return render_template(session['role'] +'phongban/form_add_thuong_phat_phong_ban.html',
                           maPB = maPB,
                           type = list(dct_type.keys()),
                           congty = session['congty'],
                           my_user = session['username'])
    
@login_required
@app.route('/view_phat_phong_ban/<string:maPB>')
def view_phat_phong_ban(maPB):
    if session['role_id'] == 3:
        abort(404)
    cur = mysql.connection.cursor()
    
    cur.execute("""SELECT *
                FROM qlnv_phongban
                WHERE MaPB = %s
                ORDER BY MaPB ASC""", (maPB, ))
    raw_data = cur.fetchall()
    
    if (len(raw_data) == 0):
        abort(404)
    
    cur.execute("""SELECT COUNT(nv.MaNhanVien)
                FROM qlnv_nhanvien nv
                RIGHT JOIN qlnv_phongban pb ON nv.MaPhongBan = pb.MaPB
                WHERE MaPB = %s
                GROUP BY MaPB
                ORDER BY MaPB ASC
                """, (maPB, ))
    count_data = cur.fetchall()[0]
    
    phongban = []
    for elm in raw_data[0]:
        phongban.append(elm)
    phongban.append(count_data[0])
    
    cur.execute("""
                SELECT COUNT(*)
                FROM qlnv_thuongphat tp
                JOIN qlnv_nhanvien nv ON tp.MaNV = nv.MaNhanVien
                WHERE nv.MaPhongBan = %s
                AND tp.Loai = 0
                ORDER BY tp.Ngay DESC
                """, (maPB, ))
    num_thuong = cur.fetchall()[0][0]
    
    cur.execute("""
                SELECT tp.* , nv.TenNV
                FROM qlnv_thuongphat tp
                JOIN qlnv_nhanvien nv ON tp.MaNV = nv.MaNhanVien
                WHERE nv.MaPhongBan = %s
                AND tp.Loai = 1
                ORDER BY tp.Ngay DESC
                """, (maPB, ))
    phat_phong_ban = cur.fetchall()
    
    return render_template(session['role'] +'phongban/view_phat_phong_ban.html',
                           num_thuong = num_thuong,
                           num_phat = len(phat_phong_ban),
                           phongban = phongban,
                           phat_phong_ban = phat_phong_ban,
                           congty = session['congty'],
                           my_user = session['username'])
    
@login_required
@app.route('/view_thuong_phong_ban/<string:maPB>')
def view_thuong_phong_ban(maPB):
    if session['role_id'] == 3:
        abort(404)
    cur = mysql.connection.cursor()
    
    cur.execute("""SELECT *
                FROM qlnv_phongban
                WHERE MaPB = %s
                ORDER BY MaPB ASC""", (maPB, ))
    raw_data = cur.fetchall()
    
    if (len(raw_data) == 0):
        abort(404)
    
    cur.execute("""SELECT COUNT(nv.MaNhanVien)
                FROM qlnv_nhanvien nv
                RIGHT JOIN qlnv_phongban pb ON nv.MaPhongBan = pb.MaPB
                WHERE MaPB = %s
                GROUP BY MaPB
                ORDER BY MaPB ASC
                """, (maPB, ))
    count_data = cur.fetchall()[0]
    
    phongban = []
    for elm in raw_data[0]:
        phongban.append(elm)
    phongban.append(count_data[0])
    
    cur.execute("""
                SELECT COUNT(*)
                FROM qlnv_thuongphat tp
                JOIN qlnv_nhanvien nv ON tp.MaNV = nv.MaNhanVien
                WHERE nv.MaPhongBan = %s
                AND tp.Loai = 1
                ORDER BY tp.Ngay DESC
                """, (maPB, ))
    num_phat = cur.fetchall()[0][0]
    
    cur.execute("""
                SELECT tp.* , nv.TenNV
                FROM qlnv_thuongphat tp
                JOIN qlnv_nhanvien nv ON tp.MaNV = nv.MaNhanVien
                WHERE nv.MaPhongBan = %s
                AND tp.Loai = 0
                ORDER BY tp.Ngay DESC
                """, (maPB, ))
    thuong_phong_ban = cur.fetchall()
    
    return render_template(session['role'] +'phongban/view_thuong_phong_ban.html',
                           num_phat = num_phat,
                           num_thuong = len(thuong_phong_ban),
                           phongban = phongban,
                           thuong_phong_ban = thuong_phong_ban,
                           congty = session['congty'],
                           my_user = session['username'])

@login_required
@app.route('/form_update_thuong_phat_phong_ban/<string:maPB>_<string:id>', methods=['GET','POST'])
def form_update_thuong_phat_phong_ban(maPB, id):
    if session['role_id'] == 3:
        abort(404)
    cur = mysql.connection.cursor()
    
    dct_type = {
        'Thưởng':0,
        'Kỷ luật':1
    }
    
    cur.execute("""
                SELECT * FROM qlnv_thuongphat
                WHERE id = %s
                """, (id, ))
    thuongphat = cur.fetchall()
    
    if (len(thuongphat) == 0):
        abort(404)
    
    thuongphat = thuongphat[0]
    
    if request.method == 'POST':
        detail = request.form
        MaNV = thuongphat[1]
        LyDo = detail['LyDo']
        Loai = dct_type[detail['Loai']]
        Tien = detail['Tien']
        Ngay = detail['Ngay']
        GhiChu = detail['GhiChu']
            
        cur.execute("""
                    UPDATE `qlnv_thuongphat` 
                    SET `Loai` = %s, `LyDo` = %s, `Tien` = %s, `Ngay` = %s, `GhiChu` = %s
                    WHERE `id` = %s;
                    """, (Loai, LyDo, Tien, Ngay, GhiChu, thuongphat[0]))
        mysql.connection.commit()
        return redirect(url_for('view_phong_ban', maPB = maPB))
    
    return render_template(session['role'] +'phongban/form_update_thuong_phat_phong_ban.html',
                           maPB = maPB,
                           type = list(dct_type.keys()),
                           thuongphat = thuongphat,
                           congty = session['congty'],
                           my_user = session['username'])
    
@login_required
@app.route('/delete_thuong_phat/<string:maPB>_<string:id>')
def delete_thuong_phat(maPB, id):
    if session['role_id'] == 3:
        abort(404)
    cur = mysql.connection.cursor()
    
    cur.execute("""
                SELECT * 
                FROM qlnv_thuongphat
                WHERE id = %s
                """, (id, ))
    if (len(cur.fetchall()) == 0):
        abort(404)
    
    cur.execute("""
                DELETE FROM qlnv_thuongphat
                WHERE id = %s
                """, (id, ))
    mysql.connection.commit()
    return redirect(url_for('view_phong_ban', maPB = maPB))
#
# ------------------ PHONG BAN ------------------------
#

#
# ------------------ HOP DONG ------------------------
#
@login_required
@app.route("/danh_sach_hop_dong")
def danh_sach_hop_dong():
    if session['role_id'] != 1:
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT * 
                FROM qlnv_hopdong
                """)
    hopdong = cur.fetchall()
    
    return render_template(session['role'] +'hopdong/danh_sach_hop_dong.html', 
                           hopdong = hopdong,
                           congty = session['congty'],
                           my_user = session['username'])


@login_required
@app.route('/form_add_hop_dong', methods=['GET','POST'])
def form_add_hop_dong():
    if session['role_id'] != 1:
        abort(404)
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        details = request.form
        MaHD = details['MaHD']
        LoaiHopDong = details['LoaiHopDong']
        NgayBatDau = details['NgayBatDau']
        NgayKetThuc = details['NgayKetThuc']
        GhiChu = details['GhiChu']
        
        cur.execute("""
                    SELECT *
                    FROM qlnv_hopdong
                    WHERE MaHopDong = %s
                    """, (MaHD, ))
        if (len(cur.fetchall()) != 0):
            return render_template(session['role'] +'hopdong/form_add_hop_dong.html', 
                                   ma_err = "Mã hợp đồng đã tồn tại",
                           congty = session['congty'],
                           my_user = session['username'])
        cur.execute("""
                    INSERT INTO `qlnv_hopdong` 
                    (`id`, `MaHopDong`, `LoaiHopDong`, `NgayBatDau`, `NgayKetThuc`, `GhiChu`) 
                    VALUES (NULL, %s, %s, %s, %s, %s);
                    """, (MaHD, LoaiHopDong, NgayBatDau, NgayKetThuc, GhiChu))
        mysql.connection.commit()
        return redirect(url_for('danh_sach_hop_dong'))
    
    return render_template(session['role'] +'hopdong/form_add_hop_dong.html', 
                           congty = session['congty'],
                           my_user = session['username'])
    

@login_required
@app.route('/delete_hop_dong/<string:id>')
def delete_hop_dong(id):
    if session['role_id'] != 1:
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute("""
                DELETE FROM qlnv_hopdong
                WHERE id = %s
                """, (id, ))
    
    mysql.connection.commit()
    return redirect(url_for('danh_sach_hop_dong'))
#
# ------------------ HOP DONG ------------------------
#


#
# ------------------ LUONG ------------------------
#

@login_required
@app.route('/table_data_money')
def table_data_money():
    if session['role_id'] != 1:
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute("""
              SELECT l.id, nv.TenNV, nv.GioiTinh, cv.TenCV, l.Thang, l.Nam,
              l.LuongChamCong, l.SoTienPhat, l.SoTienThuong, l.TongSoTien, nv.MaNhanVien
                FROM qlnv_luong l
                JOIN qlnv_nhanvien nv ON nv.MaNhanVien = l.MaNV
                JOIN qlnv_chucvu cv ON nv.MaChucVu = cv.MaCV
                ORDER BY l.Nam DESC, l.Thang DESC, l.MaNV ASC
                """)
    luong = cur.fetchall()
    return render_template(session['role'] +'luong/table_data_money.html',
                           luong = luong,
                           congty = session['congty'],
                           my_user = session['username'])

@login_required
@app.route('/view_data_money/<string:maNV>')
def view_data_money(maNV):
    cur = mysql.connection.cursor()
    
    if session['role_id'] != 1:
        cur.execute("""
            SELECT l.id,  l.Thang, l.Nam, tk.SoNgayDiLam, tk.SoNgayDiVang,
            tk.SoNgayTangCa, l.LuongCoDinh, l.LuongChamCong,
            l.SoTienPhat, l.SoTienThuong, l.TongSoTien
                FROM qlnv_luong l
                JOIN qlnv_chamcongtongketthang tk ON tk.Nam = l.Nam AND tk.Thang = l.Thang
                WHERE l.MaNV = %s AND tk.MaNhanVien = %s
                ORDER BY l.Nam DESC, l.Thang DESC
                """, (session['username'][4], session['username'][4]))
    else:
        cur.execute("""
                SELECT l.id,  l.Thang, l.Nam, tk.SoNgayDiLam, tk.SoNgayDiVang,
                tk.SoNgayTangCa, l.LuongCoDinh, l.LuongChamCong,
                l.SoTienPhat, l.SoTienThuong, l.TongSoTien
                    FROM qlnv_luong l
                    JOIN qlnv_chamcongtongketthang tk ON tk.Nam = l.Nam AND tk.Thang = l.Thang
                    WHERE l.MaNV = %s AND tk.MaNhanVien = %s
                    ORDER BY l.Nam DESC, l.Thang DESC
                    """, (maNV, maNV))
    luong = cur.fetchall()
    
    
    if session['role_id'] != 1:
        cur.execute("""
                    SELECT nv.TenNV, cv.TenCV, pb.TenPB, nv.GioiTinh
                    FROM qlnv_nhanvien nv
                    JOIN qlnv_chucvu cv ON cv.MaCV = nv.MaChucVu
                    JOIN qlnv_phongban pb ON pb.MaPB = nv.MaPhongBan
                    WHERE nv.MaNhanVien = %s
                    """, (session['username'][4], ))
    else:
        cur.execute("""
                    SELECT nv.TenNV, cv.TenCV, pb.TenPB, nv.GioiTinh
                    FROM qlnv_nhanvien nv
                    JOIN qlnv_chucvu cv ON cv.MaCV = nv.MaChucVu
                    JOIN qlnv_phongban pb ON pb.MaPB = nv.MaPhongBan
                    WHERE nv.MaNhanVien = %s
                    """, (maNV, ))
    nhanvien = cur.fetchall()
    if (len(nhanvien) == 0):
        abort(404)

    nhanvien = nhanvien[0]
    
    return render_template(session['role'] +'luong/view_data_money_one.html',
                           MaNV = maNV,
                            nhanvien = nhanvien,
                           luong = luong,
                           congty = session['congty'],
                           my_user = session['username'])
    
#
# ------------------ LUONG ------------------------
#

#
# ------------------ CaiDat ------------------------
#

@login_required
@app.route("/cai_dat")
def cai_dat():
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT COUNT(*)
                FROM qlnv_user
                """)
    so_user = cur.fetchall()[0][0]
    
    return render_template(session['role'] +'caidat/cai_dat.html', 
                           so_user = so_user,
                           congty = session['congty'],
                           my_user = session['username'])

@login_required
@app.route("/form_tao_tk", methods=['GET','POST'])
def form_tao_tk():
    if session['role_id'] != 1:
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT MaNhanVien
                FROM qlnv_nhanvien
                WHERE MaNhanVien NOT IN (
                    SELECT DISTINCT us.MaNhanVien
                    FROM qlnv_user us
                )
                """)
    nhanvien = cur.fetchall()
    
    type_account = {
        'Admin':1,
        'Trưởng Phòng':2,
        'Nhân Viên':3
    }
    
    if request.method == 'POST':
        details = request.form
        username = details['taikhoan']
        MNV = details['MNV']
        type = type_account[details['TYPE']]
        password = hashlib.md5(details['password'].encode()).hexdigest()
        password_repeat = hashlib.md5(details['password_repeat'].encode()).hexdigest()
    
        cur.execute("""
                    SELECT * 
                    FROM qlnv_user
                    WHERE username = %s
                    """, (username, ))
        if (len(cur.fetchall()) != 0):
            return render_template(session['role'] +'caidat/form_tao_tk.html',
                                my_err = "Tài khoản đã tồn tại",
                           congty = session['congty'],
                           my_user = session['username'])
    
        cur.execute("""
                    SELECT TenNV
                    FROM qlnv_nhanvien
                    WHERE MaNhanVien = %s
                    """, (MNV, ))
        this_nv = cur.fetchall()
        if (len(this_nv) != 1):
            return render_template(session['role'] +'caidat/form_tao_tk.html',
                                type_account = list(type_account.keys()),
                           nhanvien = nhanvien,
                            my_err = "Mã nhân viên không tồn tại",
                           congty = session['congty'],
                           my_user = session['username'])
        this_nv = this_nv[0]
    
        if password != password_repeat:
            return render_template(session['role'] +'caidat/form_tao_tk.html', 
                                type_account = list(type_account.keys()),
                           nhanvien = nhanvien,
                            my_err = "Nhập lại mật khẩu mới không đúng",
                           congty = session['congty'],
                           my_user = session['username'])
            
        if type == 2:
            cur.execute("""
                        SELECT *
                        FROM qlnv_phongban
                        WHERE MaTruongPhong = %s
                        """, (MNV,))
            # if (len(cur.fetchall()) == 0):
            #     return render_template(session['role'] +'caidat/form_tao_tk.html', 
            #                     type_account = list(type_account.keys()),
            #                nhanvien = nhanvien,
            #                 my_err = "Nhân viên không là trưởng phòng",
            #                congty = session['congty'],
            #                my_user = session['username'])
        
        cur.execute("""
                    INSERT INTO qlnv_user(Id_user, username, password, tennguoidung, MaNhanVien, LastLogin, register)
                    VALUES (NULL, %s, %s, %s, %s, NULL, current_timestamp())
                    """, (username, password, this_nv[0], MNV))
        mysql.connection.commit()
        
        cur.execute("""
                    SELECT Id_user
                    FROM qlnv_user
                    WHERE username = %s
                    """, (username, ))
        acc_id = cur.fetchall()[0][0]
        
        cur.execute("""
                    INSERT INTO qlnv_phanquyenuser(id_user, role_id)
                    VALUES (%s, %s)
                    """, (acc_id, type))
        mysql.connection.commit()
        return redirect(url_for('form_view_tk'))
    return render_template(session['role'] +'caidat/form_tao_tk.html', 
                           type_account = list(type_account.keys()),
                           nhanvien = nhanvien,
                           congty = session['congty'],
                           my_user = session['username'])

@login_required
@app.route("/delete_account/<string:id>")
def delete_account(id):
    if session['role_id'] != 1:
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute("""
                DELETE FROM qlnv_phanquyenuser
                WHERE id_user = %s
                """, (id, ))
    
    cur.execute("""
                DELETE FROM qlnv_user
                WHERE id_user = %s
                """, (id, ))
    mysql.connection.commit()
    return redirect(url_for('form_view_tk'))

@login_required
@app.route("/form_view_tk")
def form_view_tk():
    if session['role_id'] != 1:
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT us.Id_user, us.username, us.password, us.tennguoidung, r.role_name,
                us.MaNhanVien, us.LastLogin, us.register
                FROM qlnv_user us
                JOIN qlnv_phanquyenuser pq ON pq.id_user = us.Id_user
                JOIN qlnv_role r ON pq.role_id = r.role_id
                """)
    users = cur.fetchall()
    
    data_user_format = []
    for elm in users:
        index = 0
        tmp_data = []
        for info in elm:
            if (index != 2):
                tmp_data.append(info)
            index += 1
        data_user_format.append(tmp_data)
    return render_template(session['role'] +'caidat/form_view_tk.html', 
                           users = data_user_format,
                           congty = session['congty'],
                           my_user = session['username'])

#BE đổi mk
HCAPTCHA_SECRET = "ES_a8291e5cc4d8435ea3d34caaabab07ea"

def verify_hcaptcha(token):
    url = "https://hcaptcha.com/siteverify"
    data = {
        "secret": HCAPTCHA_SECRET,
        "response": token
    }
    r = requests.post(url, data=data)
    return r.json()


@login_required 
@app.route("/form_chinh_sua_mk/<string:id>", methods=['GET','POST'])
def form_chinh_sua_mk(id):
    cur = mysql.connection.cursor()
    if session['role_id'] != 1:
        cur.execute("""
                SELECT username
                FROM qlnv_user
                WHERE Id_user = %s
                """, (session['username'][0], ))
    else:
        cur.execute("""
                    SELECT username
                    FROM qlnv_user
                    WHERE Id_user = %s
                    """, (id, ))
    this_user = cur.fetchall()
    if (len(this_user) == 0):
        abort(404)
    this_user = this_user[0][0]
    
    if request.method == 'POST':
        # --- Check hCaptcha trước khi xử lý ---
        hcaptcha_token = request.form.get("h-captcha-response")
        result = verify_hcaptcha(hcaptcha_token)

        if not result.get("success"):
            return render_template(session['role'] +'caidat/form_chinh_sua_mk.html',
                                   role=session['role_id'],
                                   id=id,
                                   this_user=this_user,
                                   congty=session['congty'],
                                   my_user=session['username'],
                                   my_err="Xác thực hCaptcha thất bại, vui lòng thử lại")
        
        # --- Nếu captcha ok thì tiếp tục ---
        details = request.form
        old_password = ""
        if session['role_id'] != 1:
            old_password = hashlib.md5(details['password_old'].encode()).hexdigest()
        new_password = hashlib.md5(details['password'].encode()).hexdigest()
        new_password_repeat = hashlib.md5(details['password_repeat'].encode()).hexdigest()
        
        if session['role_id'] != 1:
            cur.execute("""
                        SELECT password
                        FROM qlnv_user
                        WHERE Id_user = %s
                        """, (session['username'][0], ))
            old_pass = cur.fetchall()[0][0]
            
            if old_password != old_pass:
                return render_template('caidat/form_chinh_sua_mk.html', 
                                id=session['username'][0],
                                role=session['role_id'],
                                my_err="Mật khẩu cũ không đúng",
                                this_user=this_user,
                                congty=session['congty'],
                                my_user=session['username'])
        
        if new_password != new_password_repeat:
            return render_template(session['role'] +'caidat/form_chinh_sua_mk.html', 
                            id=id,
                            role=session['role_id'],
                            my_err="Nhập lại mật khẩu mới không đúng",
                            this_user=this_user,
                            congty=session['congty'],
                            my_user=session['username'])
        
        cur.execute("""
                    UPDATE qlnv_user
                    SET password = %s
                    WHERE Id_user = %s
                    """, (new_password, id))
        mysql.connection.commit()
        if session['role_id'] != 1:
            return redirect(url_for('cai_dat'))
        return redirect(url_for('form_view_tk'))
    return render_template(session['role'] +'caidat/form_chinh_sua_mk.html', 
                           role=session['role_id'],
                           id=id,
                           this_user=this_user,
                           congty=session['congty'],
                           my_user=session['username'])

@login_required
@app.route("/form_view_cong_ty/<string:canEdit>", methods = ['GET','POST'])
def form_view_cong_ty(canEdit):
    if session['role_id'] != 1:
        abort(404)
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT * 
                FROM qlnv_congty
                """)
    lst_congty = cur.fetchall()[0]
    
    if request.method == 'POST':
        details = request.form
        TenCT = details['TenCT']
        MaSO = details['MaSO']
        NgayThanhLap = details['NgayThanhLap']
        SDT = details['SDT']
        DIACHI = details['DIACHI']
        
        image_profile = request.files['ImageProfileUpload']
        pathToImage = lst_congty[3]
        if image_profile.filename != "":
            ID_image = "logo_web"
            filename = 'favicon' + "." + secure_filename(image_profile.filename).split(".")[1]
            pathToImage = app.config['UPLOAD_FOLDER_IMG'] + "/" + filename
            image_profile.save(pathToImage)
            take_image_to_save(ID_image, pathToImage)
            pathToImage = "/".join(pathToImage.split("/")[1::])
            
        cur.execute("""
                    UPDATE qlnv_congty
                    SET TenCongTy = %s, DiaChi = %s, LogoPath = %s, SoDienThoai = %s,
                    MaSoDoanhNghiep = %s, NgayThanhLap = %s
                    WHERE ID = %s
                    """, (TenCT, DIACHI, pathToImage, SDT, MaSO, NgayThanhLap ,lst_congty[0]))
        mysql.connection.commit()
        
        cur.execute("""
                    SELECT * 
                    FROM qlnv_congty
                    """)
        session['congty'] = cur.fetchall()[0]
        return redirect(url_for('cai_dat'))
    
    if canEdit == 'E':
        return render_template(session['role'] +'caidat/form_view_cong_ty.html', 
                           mode = '',
                           lst_congty = lst_congty,
                           congty = session['congty'],
                           my_user = session['username'])
    
    return render_template(session['role'] +'caidat/form_view_cong_ty.html', 
                           mode = 'disabled',
                           lst_congty = lst_congty,
                           congty = session['congty'],
                           my_user = session['username'])

#
# ------------------ CaiDat ------------------------
#

@login_required
@app.route("/index")
def index():
    return render_template(session['role'] +'index.html', 
                           congty = session['congty'],
                           my_user = session['username'])


# Error Handler
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html',
                           error = error), 404
@app.errorhandler(500)
def no_role_access(error):
    return render_template('error.html',
                           error = error), 404

def take_image_to_save(id_image, path_to_img):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM qlnv_imagedata""")
    img_data = cur.fetchall()
    change_path = False
    
    path_to_img = "/".join(path_to_img.split("/")[1::])
    
    for data in img_data:
        if id_image in data:
            change_path = True
            if os.path.exists(data[1]):
                os.remove(data[1])
            break;
    
    if change_path:
        sql = """
            UPDATE qlnv_imagedata
            SET PathToImage = %s
            WHERE ID_image = %s"""
        val = (id_image, path_to_img)
        cur.execute(sql,val)
        mysql.connection.commit()
        return True
    
    sql = """
        INSERT INTO qlnv_imagedata (ID_image, PathToImage) 
        VALUES (%s, %s)"""
    val = (id_image, path_to_img)
    cur.execute(sql,val)
    mysql.connection.commit()
    return True;
    