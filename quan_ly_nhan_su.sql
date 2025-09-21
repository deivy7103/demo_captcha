-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th4 03, 2025 lúc 04:52 PM
-- Phiên bản máy phục vụ: 11.7.2-MariaDB
-- Phiên bản PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `quan_ly_nhan_su`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_nhanvien`
--

CREATE TABLE `qlnv_nhanvien` (
  `MaNhanVien` varchar(8) NOT NULL,
  `MaChucVu` varchar(8) NOT NULL,
  `MaPhongBan` varchar(8) NOT NULL,
  `Luong` double NOT NULL,
  `GioiTinh` varchar(4) NOT NULL DEFAULT 'Nam',
  `MaHD` varchar(8) NOT NULL,
  `TenNV` varchar(50) NOT NULL,
  `NgaySinh` date NOT NULL,
  `NoiSinh` varchar(100) NOT NULL,
  `SoCMT` varchar(20) NOT NULL,
  `DienThoai` varchar(20) NOT NULL,
  `DiaChi` varchar(250) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `TTHonNhan` varchar(20) NOT NULL DEFAULT 'Độc thân',
  `DanToc` varchar(10) DEFAULT 'Kinh',
  `MATDHV` varchar(8) DEFAULT NULL,
  `NgayCMND` date DEFAULT NULL,
  `NoiCMND` varchar(50) DEFAULT NULL,
  `BHYT` varchar(15) NOT NULL,
  `BHXH` varchar(15) NOT NULL,
  `ID_profile_image` varchar(40) NOT NULL DEFAULT 'none_image_profile'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_nhanvien`
--

INSERT INTO `qlnv_nhanvien` (`MaNhanVien`, `MaChucVu`, `MaPhongBan`, `Luong`, `GioiTinh`, `MaHD`, `TenNV`, `NgaySinh`, `NoiSinh`, `SoCMT`, `DienThoai`, `DiaChi`, `Email`, `TTHonNhan`, `DanToc`, `MATDHV`, `NgayCMND`, `NoiCMND`, `BHYT`, `BHXH`, `ID_profile_image`) VALUES
('NV000', 'GD', 'PBGD', 50000000, 'Nam', 'HD000', 'Trần Chủ Tịch', '1999-12-12', 'Phú Lạc - Đại Từ - Thái Nguyên', '019204555442', '0336258741', 'Hà Đông - Hà Nội', 'Tichct@gmail.com', 'Độc thân', 'Kinh', 'TS001', '2021-05-21', 'Hà Đông', '0123456445', '01122556998', 'Image_Profile_NV000'),
('NV001', 'NV', 'MPB02', 15000000, 'Nam', 'HD001', 'Hoàng Huy Phong', '2001-03-31', 'Phú Xuyên - Đại Từ - Thái Nguyên', '019204011999', '0333986331', 'Yên Xá - Tân Triều - Thanh Trì - Hà Nội', 'PhongHH@gmail.com', 'Đã kết hôn', 'Kinh', 'TNKHMTTT', '2022-05-14', 'Đại Từ', '0123456789', '01122334455', 'Image_Profile_NV001'),
('NV002', 'GD', 'PBGD', 25000000, 'Nữ', 'HD002', 'Vũ Thanh Vân', '1996-05-12', 'Nguyễn Trãi - Hà Đông - Hà Nội', '019996336552', '0333986442', 'tp Hồ Chí Minh', 'VanVT@gmail.com', 'Độc thân', 'Kinh', 'TS001', '2021-05-14', 'Hà Đông', '0123456798', '01122336622', 'Image_Profile_NV002'),
('NV003', 'NV', 'MPB05', 20000000, 'Nam', 'HD003', 'Nguyễn Đức Cường', '1989-11-12', 'Uông Bí - Quảng Ninh', '019989369852', '0334568923', 'Hạ Long - Quang Ninh', 'denVau@gmail.com', 'Đã kết hôn', 'Tày', 'TNKHMTTT', '2021-06-05', 'Uông Bí', '0123456546', '01122556623', 'Image_Profile_NV003'),
('NV004', 'TTS', 'MPB02', 5000000, 'Nam', 'HD004', 'Nguyễn Minh Nam', '2004-01-07', 'Phú Lạc - Đại Từ - Thái Nguyên', '0192055211999', '0334568745', 'Hà Đông - Hà Nội', 'nguyenquanghuy@gmail.com', 'Độc thân', 'Kinh', 'SV001', '2022-05-21', 'Hà Đông', '0563456445', '01141256623', 'none_image_profile'),
('NV005', 'NV', 'MPB03', 20000000, 'Nữ', 'HD005', 'Nguyễn Minh Ngọc', '2000-06-23', 'Văn Quán - Hà Đông', '019200555685', '0333444555', 'Văn Quán - Hà Đông', 'ngocnm@gmail.com', 'Độc thân', 'Kinh', 'TS001', '2021-05-14', 'Hà Đông', '2255669854', '124587963', 'none_image_profile');

--
-- Bẫy `qlnv_nhanvien`
--
DELIMITER $$
CREATE TRIGGER `befor_update_nhanvien` BEFORE UPDATE ON `qlnv_nhanvien` FOR EACH ROW BEGIN
    IF NEW.MaChucVu != OLD.MaChucVu THEN
    	UPDATE qlnv_thoigiancongtac tg SET tg.DuongNhiem = 0, tg.NgayKetThuc = CURRENT_DATE() WHERE tg.MaNV = OLD.MaNhanVien AND tg.DuongNhiem = 1;
        INSERT INTO qlnv_thoigiancongtac(MaNV, MaCV, NgayNhanChuc, NgayKetThuc, DuongNhiem) VALUES (OLD.MaNhanVien, NEW.MaChucVu, CURRENT_DATE(), NULL, '1');   	
        
    END IF;
END
$$
DELIMITER ;

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `qlnv_nhanvien`
--
ALTER TABLE `qlnv_nhanvien`
  ADD PRIMARY KEY (`MaNhanVien`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;