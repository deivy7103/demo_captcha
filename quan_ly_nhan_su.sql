-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th9 29, 2025 lúc 04:37 AM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
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
-- Cấu trúc bảng cho bảng `qlnv_chamcong`
--

CREATE TABLE `qlnv_chamcong` (
  `id` int(11) NOT NULL,
  `MaNV` varchar(8) NOT NULL,
  `Ngay` date NOT NULL,
  `GioVao` time NOT NULL,
  `GioRa` time NOT NULL,
  `OT` tinyint(1) NOT NULL,
  `ThoiGianLamViec` time NOT NULL,
  `ThoiGian_thap_phan` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_chamcong`
--

INSERT INTO `qlnv_chamcong` (`id`, `MaNV`, `Ngay`, `GioVao`, `GioRa`, `OT`, `ThoiGianLamViec`, `ThoiGian_thap_phan`) VALUES
(54, 'MNV03', '2024-12-17', '07:30:00', '11:50:00', 0, '04:20:00', 4.3),
(55, 'MNV03', '2024-12-11', '07:30:00', '11:30:00', 0, '04:00:00', 4),
(60, 'MNV01', '2024-11-02', '07:30:00', '11:30:00', 0, '04:00:00', 4),
(62, 'MNV03', '2024-11-01', '07:30:00', '10:30:00', 0, '03:00:00', 3),
(63, 'MNV02', '2024-12-01', '07:30:00', '11:30:00', 0, '04:00:00', 4),
(64, 'MNV01', '2024-11-01', '07:30:00', '11:30:00', 0, '04:00:00', 4),
(65, 'MNV03', '2024-12-03', '07:30:00', '11:50:00', 0, '04:20:00', 4.3),
(66, 'MNV03', '2024-12-04', '07:30:00', '11:30:00', 0, '04:00:00', 4),
(67, 'MNV03', '2024-12-04', '13:30:00', '17:00:00', 0, '03:30:00', 3.5),
(68, 'MNV02', '2024-12-02', '07:30:00', '11:50:00', 0, '04:20:00', 4.3),
(69, 'MNV02', '2024-12-03', '07:30:00', '11:50:00', 0, '04:20:00', 4.3),
(70, 'MNV03', '2024-10-01', '07:30:00', '11:00:00', 0, '03:30:00', 3.5),
(71, 'MNV03', '2024-10-02', '07:30:00', '11:30:00', 0, '04:00:00', 4),
(72, 'MNV03', '2024-12-03', '07:30:00', '10:15:00', 0, '02:45:00', 2.8),
(73, 'MNV02', '2024-11-01', '07:30:00', '11:50:00', 0, '04:20:00', 4.3),
(74, 'MNV02', '2024-11-18', '07:30:00', '11:50:00', 0, '04:20:00', 4.3),
(75, 'MNV02', '2024-12-25', '16:14:29', '16:21:13', 0, '00:06:44', 0.1),
(76, 'MNV01', '2024-12-25', '20:49:26', '20:52:22', 0, '00:02:56', 0),
(77, 'MNV05', '2024-04-10', '08:00:00', '17:00:00', 0, '09:00:00', 9),
(78, 'MNV01', '2025-04-01', '08:00:00', '11:00:00', 0, '03:00:00', 3),
(79, 'MNV01', '2025-04-01', '13:00:00', '18:00:00', 0, '05:00:00', 5),
(80, 'MNV01', '2025-04-02', '09:00:00', '15:00:00', 0, '06:00:00', 6),
(81, 'MNV01', '2025-04-03', '08:00:00', '16:00:00', 0, '08:00:00', 8),
(82, 'MNV01', '2025-04-04', '08:00:00', '15:00:00', 0, '07:00:00', 7),
(83, 'MNV01', '2025-04-05', '09:00:00', '17:00:00', 0, '08:00:00', 8),
(84, 'MNV01', '2025-04-06', '08:00:00', '15:00:00', 0, '07:00:00', 7),
(85, 'MNV01', '2025-04-07', '09:00:00', '17:00:00', 0, '08:00:00', 8),
(86, 'MNV01', '2025-04-08', '08:00:00', '11:00:00', 0, '03:00:00', 3),
(87, 'MNV01', '2025-04-08', '13:00:00', '18:00:00', 0, '05:00:00', 5),
(88, 'MNV01', '2025-04-09', '09:00:00', '17:00:00', 0, '08:00:00', 8),
(89, 'MNV01', '2025-04-10', '08:00:00', '16:00:00', 0, '08:00:00', 8),
(90, 'MNV01', '2025-04-11', '06:00:00', '10:00:00', 0, '04:00:00', 4),
(91, 'MNV01', '2025-04-11', '14:00:00', '18:00:00', 0, '04:00:00', 4),
(92, 'MNV02', '2025-05-08', '08:00:00', '16:00:00', 0, '08:00:00', 8),
(93, 'MNV02', '2025-05-07', '08:00:00', '18:00:00', 0, '10:00:00', 10),
(94, 'MNV01', '2025-09-16', '22:36:48', '22:36:53', 0, '00:00:05', 0);

--
-- Bẫy `qlnv_chamcong`
--
DELIMITER $$
CREATE TRIGGER `before_insert_to_cham_cong` BEFORE INSERT ON `qlnv_chamcong` FOR EACH ROW BEGIN
       		IF (NEW.GioRa > NEW.GioVao) THEN
           		SET NEW.ThoiGianLamViec = TIMEDIFF(NEW.GioRa,NEW.GioVao);
                SET NEW.ThoiGian_thap_phan =   ROUND(CAST(LEFT(NEW.ThoiGianLamViec, 2) AS int) +
    CAST(SUBSTRING(NEW.ThoiGianLamViec, 4, 2) AS int) / 60.0 +
    CAST(SUBSTRING(NEW.ThoiGianLamViec, 7, 2) AS int) / (60.0*60.0),1);
            ELSE
            	SET NEW.ThoiGianLamViec = 0;
                SET NEW.ThoiGian_thap_phan = 0;
            END IF;
       END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `before_update_to_cham_cong` BEFORE UPDATE ON `qlnv_chamcong` FOR EACH ROW BEGIN
       		IF (NEW.GioRa > NEW.GioVao) THEN
           		SET NEW.ThoiGianLamViec = TIMEDIFF(NEW.GioRa,NEW.GioVao);
                SET NEW.ThoiGian_thap_phan =   ROUND(CAST(LEFT(NEW.ThoiGianLamViec, 2) AS int) +
    CAST(SUBSTRING(NEW.ThoiGianLamViec, 4, 2) AS int) / 60.0 +
    CAST(SUBSTRING(NEW.ThoiGianLamViec, 7, 2) AS int) / (60.0*60.0),1);
            ELSE
            	SET NEW.ThoiGianLamViec = 0;
                SET NEW.ThoiGian_thap_phan = 0;
            END IF;
       END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_chamcongngay`
--

CREATE TABLE `qlnv_chamcongngay` (
  `MaChamCong` int(11) NOT NULL,
  `MaNV` varchar(8) NOT NULL,
  `Nam` year(4) NOT NULL DEFAULT current_timestamp(),
  `Thang` int(11) NOT NULL,
  `SoNgayThang` int(11) NOT NULL,
  `Ngay1` float NOT NULL DEFAULT -1,
  `Ngay2` float NOT NULL DEFAULT -1,
  `Ngay3` float NOT NULL DEFAULT -1,
  `Ngay4` float NOT NULL DEFAULT -1,
  `Ngay5` float NOT NULL DEFAULT -1,
  `Ngay6` float NOT NULL DEFAULT -1,
  `Ngay7` float NOT NULL DEFAULT -1,
  `Ngay8` float NOT NULL DEFAULT -1,
  `Ngay9` float NOT NULL DEFAULT -1,
  `Ngay10` float NOT NULL DEFAULT -1,
  `Ngay11` float NOT NULL DEFAULT -1,
  `Ngay12` float NOT NULL DEFAULT -1,
  `Ngay13` float NOT NULL DEFAULT -1,
  `Ngay14` float NOT NULL DEFAULT -1,
  `Ngay15` float NOT NULL DEFAULT -1,
  `Ngay16` float NOT NULL DEFAULT -1,
  `Ngay17` float NOT NULL DEFAULT -1,
  `Ngay18` float NOT NULL DEFAULT -1,
  `Ngay19` float NOT NULL DEFAULT -1,
  `Ngay20` float NOT NULL DEFAULT -1,
  `Ngay21` float NOT NULL DEFAULT -1,
  `Ngay22` float NOT NULL DEFAULT -1,
  `Ngay23` float NOT NULL DEFAULT -1,
  `Ngay24` float NOT NULL DEFAULT -1,
  `Ngay25` float NOT NULL DEFAULT -1,
  `Ngay26` float NOT NULL DEFAULT -1,
  `Ngay27` float NOT NULL DEFAULT -1,
  `Ngay28` float NOT NULL DEFAULT -1,
  `Ngay29` float NOT NULL DEFAULT -1,
  `Ngay30` float NOT NULL DEFAULT -1,
  `Ngay31` float NOT NULL DEFAULT -1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_chamcongngay`
--

INSERT INTO `qlnv_chamcongngay` (`MaChamCong`, `MaNV`, `Nam`, `Thang`, `SoNgayThang`, `Ngay1`, `Ngay2`, `Ngay3`, `Ngay4`, `Ngay5`, `Ngay6`, `Ngay7`, `Ngay8`, `Ngay9`, `Ngay10`, `Ngay11`, `Ngay12`, `Ngay13`, `Ngay14`, `Ngay15`, `Ngay16`, `Ngay17`, `Ngay18`, `Ngay19`, `Ngay20`, `Ngay21`, `Ngay22`, `Ngay23`, `Ngay24`, `Ngay25`, `Ngay26`, `Ngay27`, `Ngay28`, `Ngay29`, `Ngay30`, `Ngay31`) VALUES
(41, 'MNV03', '2024', 12, 31, -1, -1, 7.1, 7.5, -1, -1, -1, -1, -1, -1, 4, -1, -1, -1, -1, -1, 4.3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(45, 'MNV01', '2024', 11, 30, 4, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(47, 'MNV03', '2024', 11, 30, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(48, 'MNV02', '2024', 12, 31, 4, 4.3, 4.3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0.1, -1, -1, -1, -1, -1, -1),
(49, 'MNV03', '2024', 10, 31, 3.5, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(50, 'MNV02', '2024', 11, 30, 4.3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4.3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(51, 'MNV01', '2024', 12, 31, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1),
(52, 'MNV05', '2024', 4, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(53, 'MNV01', '2025', 4, 30, 8, 6, 8, 7, 8, 7, 8, 8, 8, 8, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(54, 'MNV02', '2025', 5, 31, -1, -1, -1, -1, -1, -1, 10, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1),
(55, 'MNV01', '2025', 9, 30, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_chamcongthang`
--

CREATE TABLE `qlnv_chamcongthang` (
  `id` int(11) NOT NULL,
  `MaNV` varchar(8) NOT NULL,
  `Nam` year(4) NOT NULL DEFAULT current_timestamp(),
  `T1` float NOT NULL DEFAULT -1,
  `T2` float NOT NULL DEFAULT -1,
  `T3` float NOT NULL DEFAULT -1,
  `T4` float NOT NULL DEFAULT -1,
  `T5` float NOT NULL DEFAULT -1,
  `T6` float NOT NULL DEFAULT -1,
  `T7` float NOT NULL DEFAULT -1,
  `T8` float NOT NULL DEFAULT -1,
  `T9` float NOT NULL DEFAULT -1,
  `T10` float NOT NULL DEFAULT -1,
  `T11` float NOT NULL DEFAULT -1,
  `T12` float NOT NULL DEFAULT -1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_chamcongthang`
--

INSERT INTO `qlnv_chamcongthang` (`id`, `MaNV`, `Nam`, `T1`, `T2`, `T3`, `T4`, `T5`, `T6`, `T7`, `T8`, `T9`, `T10`, `T11`, `T12`) VALUES
(21, 'MNV03', '2024', -1, -1, -1, -1, -1, -1, -1, -1, -1, 7.5, 3, 22.9),
(25, 'MNV01', '2024', -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, 0),
(27, 'MNV02', '2024', -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8.6, 12.7),
(28, 'MNV05', '2024', -1, -1, -1, 9, -1, -1, -1, -1, -1, -1, -1, -1),
(29, 'MNV01', '2025', -1, -1, -1, 84, -1, -1, -1, -1, 0, -1, -1, -1),
(30, 'MNV02', '2025', -1, -1, -1, -1, 18, -1, -1, -1, -1, -1, -1, -1);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_chamcongtongketthang`
--

CREATE TABLE `qlnv_chamcongtongketthang` (
  `Id` int(11) NOT NULL,
  `MaNhanVien` varchar(8) NOT NULL,
  `Nam` year(4) NOT NULL,
  `Thang` int(11) NOT NULL,
  `SoNgayDiLam` int(11) NOT NULL DEFAULT 0,
  `SoNgayDiVang` int(11) NOT NULL DEFAULT 0,
  `SoNgayTangCa` int(11) NOT NULL DEFAULT 0,
  `TongSoNgay` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_chamcongtongketthang`
--

INSERT INTO `qlnv_chamcongtongketthang` (`Id`, `MaNhanVien`, `Nam`, `Thang`, `SoNgayDiLam`, `SoNgayDiVang`, `SoNgayTangCa`, `TongSoNgay`) VALUES
(19, 'MNV03', '2024', 12, 4, 23, 0, 4),
(23, 'MNV01', '2024', 11, 2, 24, 0, 2),
(24, 'MNV03', '2024', 11, 1, 25, 0, 1),
(25, 'MNV02', '2024', 12, 4, 23, 0, 4),
(26, 'MNV03', '2024', 10, 2, 24, 0, 2),
(27, 'MNV02', '2024', 11, 2, 24, 0, 2),
(28, 'MNV01', '2024', 12, 1, 26, 0, 1),
(29, 'MNV05', '2024', 4, 1, 25, 0, 1),
(30, 'MNV01', '2025', 4, 11, 15, 0, 11),
(31, 'MNV02', '2025', 5, 2, 25, 0, 2),
(32, 'MNV01', '2025', 9, 1, 25, 0, 1);

--
-- Bẫy `qlnv_chamcongtongketthang`
--
DELIMITER $$
CREATE TRIGGER `delete_tongket_luong` BEFORE DELETE ON `qlnv_chamcongtongketthang` FOR EACH ROW BEGIN
    DELETE FROM `qlnv_luong`
    WHERE MaNV = OLD.MaNhanVien AND Nam = OLD.Nam AND Thang = OLD.Thang;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `insert_data_tongket_tinh_luong` BEFORE INSERT ON `qlnv_chamcongtongketthang` FOR EACH ROW BEGIN
	DECLARE tongthoigian integer;
    DECLARE luongDuocNhan double;
    DECLARE tongsogiophailam integer;
    DECLARE sotienphat double;
     DECLARE sotienthuong double;
     DECLARE luongCoDinh double;
     DECLARE luongchamcong double;
    SET tongsogiophailam = (NEW.SoNgayDiLam + NEW.SoNgayDiVang) * 8;
    
    IF (NEW.Thang = 1) THEN
    	SET tongthoigian = (SELECT cct.T1 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
    ELSEIF (NEW.Thang = 2) THEN
    	SET tongthoigian = (SELECT cct.T2 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 3) THEN
    	SET tongthoigian = (SELECT cct.T3 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 4) THEN
    	SET tongthoigian = (SELECT cct.T4 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 5) THEN
    	SET tongthoigian = (SELECT cct.T5 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 6) THEN
    	SET tongthoigian = (SELECT cct.T6 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 7) THEN
    	SET tongthoigian = (SELECT cct.T7 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 8) THEN
    	SET tongthoigian = (SELECT cct.T8 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 9) THEN
    	SET tongthoigian = (SELECT cct.T9 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 10) THEN
    	SET tongthoigian = (SELECT cct.T10 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 11) THEN
    	SET tongthoigian = (SELECT cct.T11 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSE
    	SET tongthoigian = (SELECT cct.T12 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	END IF;
    
    
    SET luongCoDinh = (SELECT nv.Luong FROM qlnv_nhanvien nv WHERE nv.MaNhanVien = NEW.MaNhanVien);
    
    
    IF (tongthoigian >= 0.85 * tongsogiophailam) THEN
    	SET luongchamcong = luongCoDinh;
    ELSE 
    	SET luongchamcong = ROUND((tongthoigian * luongCoDinh)/(0.85 * tongsogiophailam),-3);
    END IF;
    
    
    SET sotienphat = (SELECT SUM(tp.Tien) 
                      FROM qlnv_thuongphat tp 
                      WHERE tp.MaNV = NEW.MaNhanVien AND MONTH(tp.Ngay) = NEW.Thang
                     AND YEAR(tp.Ngay) = NEW.Nam AND tp.Loai = 1);
    
    IF sotienphat IS NULL THEN
    	SET sotienphat = 0;
     END IF;
    
   
    set sotienthuong = (SELECT SUM(tp.Tien) 
                      FROM qlnv_thuongphat tp 
                      WHERE tp.MaNV = NEW.MaNhanVien AND MONTH(tp.Ngay) = NEW.Thang
                     AND YEAR(tp.Ngay) = NEW.Nam AND tp.Loai = 0);
                     
    IF sotienthuong IS NULL THEN
    	SET sotienthuong = 0;
     END IF;
    
    
    SET luongDuocNhan = ROUND(luongchamcong - sotienphat + sotienthuong, -3);
    
    INSERT INTO `qlnv_luong` (`id`, `MaNV`, `Nam`, `Thang`, `LuongCoDinh`, `LuongChamCong`, `SoTienThuong`, `SoTienPhat`, `TongSoTien`) 
    VALUES (NULL, NEW.MaNhanVien, NEW.Nam, New.Thang, luongCoDinh, luongchamcong, sotienthuong, sotienphat, luongDuocNhan);
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `update_tongketthang_luong` AFTER UPDATE ON `qlnv_chamcongtongketthang` FOR EACH ROW BEGIN
	DECLARE tongthoigian integer;
    DECLARE luongCoDinh double;
    DECLARE tongsogiophailam integer;
    DECLARE sotienphat double;
    DECLARE luongchamcong double;
    DECLARE luongDuocNhan double;
    DECLARE sotienthuong double;
    
    SET tongsogiophailam = (NEW.SoNgayDiLam + NEW.SoNgayDiVang) * 8;
    
    IF (NEW.Thang = 1) THEN
    	SET tongthoigian = (SELECT cct.T1 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
    ELSEIF (NEW.Thang = 2) THEN
    	SET tongthoigian = (SELECT cct.T2 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 3) THEN
    	SET tongthoigian = (SELECT cct.T3 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 4) THEN
    	SET tongthoigian = (SELECT cct.T4 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 5) THEN
    	SET tongthoigian = (SELECT cct.T5 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 6) THEN
    	SET tongthoigian = (SELECT cct.T6 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 7) THEN
    	SET tongthoigian = (SELECT cct.T7 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 8) THEN
    	SET tongthoigian = (SELECT cct.T8 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 9) THEN
    	SET tongthoigian = (SELECT cct.T9 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 10) THEN
    	SET tongthoigian = (SELECT cct.T10 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSEIF (NEW.Thang = 11) THEN
    	SET tongthoigian = (SELECT cct.T11 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	ELSE
    	SET tongthoigian = (SELECT cct.T12 FROM qlnv_chamcongthang cct WHERE cct.Nam = NEW.Nam AND NEW.MaNhanVien = cct.MaNV);
	END IF;
    
    
    SET luongCoDinh = (SELECT l.LuongCoDinh FROM qlnv_luong l WHERE NEW.MaNhanVien = l.MaNV AND NEW.Nam = l.Nam AND New.Thang = l.Thang);
    
    
    IF (tongthoigian >= 0.85 * tongsogiophailam) THEN
    	SET luongchamcong = luongCoDinh;
    ELSE 
    	SET luongchamcong = ROUND((tongthoigian * luongCoDinh)/(0.85 * tongsogiophailam),-3);
    END IF;
    
    
    SET sotienphat = (SELECT SUM(tp.Tien) 
                      FROM qlnv_thuongphat tp 
                      WHERE tp.MaNV = NEW.MaNhanVien AND MONTH(tp.Ngay) = NEW.Thang
                     AND YEAR(tp.Ngay) = NEW.Nam AND tp.Loai = 1);
    
    IF sotienphat IS NULL THEN
    	SET sotienphat = 0;
     END IF;
    
  
    set sotienthuong = (SELECT SUM(tp.Tien) 
                      FROM qlnv_thuongphat tp 
                      WHERE tp.MaNV = NEW.MaNhanVien AND MONTH(tp.Ngay) = NEW.Thang
                     AND YEAR(tp.Ngay) = NEW.Nam AND tp.Loai = 0);
                     
    IF sotienthuong IS NULL THEN
    	SET sotienthuong = 0;
     END IF;
    
    SET luongDuocNhan = ROUND(luongchamcong - sotienphat + sotienthuong, -3);
    
    UPDATE `qlnv_luong`
    SET `LuongChamCong`= luongchamcong, `SoTienThuong` = sotienthuong, `SoTienPhat` = sotienphat, `TongSoTien` = luongDuocNhan
    WHERE MaNV = NEW.MaNhanVien AND Nam = NEW.Nam AND Thang = New.Thang;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_chucvu`
--

CREATE TABLE `qlnv_chucvu` (
  `MaCV` varchar(8) NOT NULL,
  `TenCV` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_chucvu`
--

INSERT INTO `qlnv_chucvu` (`MaCV`, `TenCV`) VALUES
('GD', 'Giám đốc'),
('NV', 'Nhân viên'),
('NVBH', 'Nhân viên bán hàng'),
('NVTV', 'Nhân viên tư vấn'),
('TP', 'Trưởng phòng'),
('TTa', 'Tổ trưởng A'),
('TTS', 'Thực tập sinh');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_congty`
--

CREATE TABLE `qlnv_congty` (
  `ID` int(11) NOT NULL,
  `TenCongTy` varchar(100) NOT NULL,
  `DiaChi` varchar(100) NOT NULL,
  `LogoPath` varchar(100) NOT NULL,
  `SoDienThoai` varchar(11) NOT NULL,
  `MaSoDoanhNghiep` varchar(20) NOT NULL,
  `NgayThanhLap` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_congty`
--

INSERT INTO `qlnv_congty` (`ID`, `TenCongTy`, `DiaChi`, `LogoPath`, `SoDienThoai`, `MaSoDoanhNghiep`, `NgayThanhLap`) VALUES
(1, 'Công ty quản lý nhân sự PTIT', 'Nguyễn Trãi, Hà Đông, Hà Nội', 'web/img/favicon.png', '0123456789', '0987654321', '2025-03-15');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_hopdong`
--

CREATE TABLE `qlnv_hopdong` (
  `id` int(11) NOT NULL,
  `MaHopDong` varchar(8) NOT NULL,
  `LoaiHopDong` varchar(30) NOT NULL,
  `NgayBatDau` date NOT NULL,
  `NgayKetThuc` date DEFAULT NULL,
  `GhiChu` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_hopdong`
--

INSERT INTO `qlnv_hopdong` (`id`, `MaHopDong`, `LoaiHopDong`, `NgayBatDau`, `NgayKetThuc`, `GhiChu`) VALUES
(1, 'MHDMN11', 'Nhân viên', '2024-12-13', NULL, 'Hợp đồng cho nhân viên Nguyễn Quang Huy - MNN00'),
(2, 'MHD01', 'Thực tập sinh', '2024-10-01', NULL, 'Hợp đồng cho thực tập sinh Hoàng Huy Phong - MNV01'),
(3, 'MHD02', 'Thực tập sinh', '2024-11-02', NULL, 'Hợp đồng cho thực tập sinh Nguyễn Minh Nam - MNV02'),
(4, 'MHD03', 'Thực tập sinh', '2024-11-02', NULL, 'Hợp đồng cho thực tập sinh Phạm Văn Doanh - MNV03'),
(5, 'MHD04', 'Giám đốc', '2024-12-01', NULL, 'Hợp đồng thuê giám đốc'),
(6, 'MHD05', 'Trưởng phòng', '2024-12-01', NULL, 'Hợp đồng trưởng phòng cho Hoàng Anh Khoa'),
(7, 'MHD06', 'Nhân viên', '2024-10-04', NULL, 'Hợp đồng nhân viên cho Đặng Minh Khôi'),
(8, 'MHD07', 'Nhân viên', '2024-10-04', NULL, 'Hợp đồng nhân viên cho Trần Minh Khôi'),
(9, 'MHD08', 'Nhân viên', '2024-10-10', NULL, 'Hợp đồng nhân viên cho Nguyễn Minh Khôi'),
(10, 'HDMNV10', 'Nhân viên', '2024-12-13', NULL, 'Hợp đồng nhân viên cho Lê Minh Khôi'),
(11, 'HDMNV12', 'Thực tập sinh', '2024-12-13', NULL, 'Hợp đồng thực tập sinh cho Trần Anh Khoa');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_imagedata`
--

CREATE TABLE `qlnv_imagedata` (
  `ID_image` varchar(40) NOT NULL,
  `PathToImage` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_imagedata`
--

INSERT INTO `qlnv_imagedata` (`ID_image`, `PathToImage`) VALUES
('Image_Profile_MNV01', 'web/img/Image_Profile_MNV01.jpg'),
('Image_Profile_MNV02', 'web/img/Image_Profile_MNV02.gif'),
('Image_Profile_MNV03', 'web/img/Image_Profile_MNV03.jpg'),
('Image_Profile_MNV04', 'web/img/Image_Profile_MNV04.jpg'),
('Image_Profile_MNV37', 'web/img/Image_Profile_MNV37.png'),
('logo_web', 'web/img/favicon.png'),
('none_image_profile', 'web/img/No_Image.png');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_luong`
--

CREATE TABLE `qlnv_luong` (
  `id` int(11) NOT NULL,
  `MaNV` varchar(8) NOT NULL,
  `Nam` year(4) NOT NULL,
  `Thang` int(11) NOT NULL,
  `LuongCoDinh` double NOT NULL,
  `LuongChamCong` double NOT NULL,
  `SoTienThuong` double NOT NULL DEFAULT 0,
  `SoTienPhat` double NOT NULL DEFAULT 0,
  `TongSoTien` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_luong`
--

INSERT INTO `qlnv_luong` (`id`, `MaNV`, `Nam`, `Thang`, `LuongCoDinh`, `LuongChamCong`, `SoTienThuong`, `SoTienPhat`, `TongSoTien`) VALUES
(6, 'MNV03', '2024', 12, 1000000, 125000, 20000, 10000, 135000),
(7, 'MNV01', '2024', 11, 1000000, 45000, 0, 0, 45000),
(8, 'MNV03', '2024', 11, 1000000, 17000, 0, 0, 17000),
(9, 'MNV02', '2024', 12, 1000000, 71000, 10000, 0, 81000),
(10, 'MNV03', '2024', 10, 1000000, 45000, 0, 0, 45000),
(11, 'MNV02', '2024', 11, 1000000, 51000, 0, 0, 51000),
(12, 'MNV01', '2024', 12, 1000000, 0, 0, 0, 0),
(13, 'MNV05', '2024', 4, 900000, 46000, 0, 0, 46000),
(14, 'MNV01', '2025', 4, 1000000, 475000, 0, 0, 475000),
(15, 'MNV02', '2025', 5, 1000000, 98000, 0, 0, 98000),
(16, 'MNV01', '2025', 9, 1000000, 0, 0, 0, 0);

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_nhanvien`
--

INSERT INTO `qlnv_nhanvien` (`MaNhanVien`, `MaChucVu`, `MaPhongBan`, `Luong`, `GioiTinh`, `MaHD`, `TenNV`, `NgaySinh`, `NoiSinh`, `SoCMT`, `DienThoai`, `DiaChi`, `Email`, `TTHonNhan`, `DanToc`, `MATDHV`, `NgayCMND`, `NoiCMND`, `BHYT`, `BHXH`, `ID_profile_image`) VALUES
('MNN00', 'NV', 'MPB05', 13000000, 'Nam', 'MHDMN11', 'Nguyễn Quang Huy', '2004-12-12', 'Đại Từ - Thái Nguyên', '019204211633', '0335698741', 'Hà Đông - Hà Nội', 'nguyenquanghuy@gmail.com', 'Độc thân', 'Kinh', 'SV002', '2021-03-10', 'Đại từ', 'SV40101206185', '0118059003', 'none_image_profile'),
('MNV01', 'TTS', 'MPB01', 1000000, 'Nam', 'MHD01', 'Nguyễn Thanh Tùng', '2004-01-07', 'Hiệp Hòa - Bắc Giang', '001215387168', '0877625245', 'Hiệp Hòa - Bắc Giang', 'tungnt@gmail.com', 'Độc thân', 'Kinh', 'SV001', '2021-11-30', 'Hiệp Hòa - Bắc Giang', 'SV40101238294', '0118128311', 'Image_Profile_MNV01'),
('MNV02', 'TTS', 'MPB02', 1000000, 'Nam', 'MHD02', 'Nguyễn Minh Nam', '2004-11-28', 'Hà Tây', '001202035197', '0945549876', 'Hà Đông - Hà Nội', 'namnm@gmail.com', 'Độc thân', 'Kinh', 'SV001', '2021-08-03', 'Hà Nội', 'SV401985718', '0118157171', 'Image_Profile_MNV02'),
('MNV03', 'TTS', 'MPB01', 1000000, 'Nam', 'MHD03', 'Phạm Văn Doanh', '2003-04-04', 'Phú Thọ', '123456789', '0822655245', 'Thanh Xuân, Hà Nội', 'doanhph@gmail.com', 'Đã kết hôn', 'Kinh', 'SV001', '2020-12-12', 'Phú Thọ', 'SV40101135729', '0811002892', 'Image_Profile_MNV03'),
('MNV04', 'GD', 'PBGD', 10000000, 'Nam', 'MHD04', 'Phùng Khánh Linh', '1994-08-05', 'Bắc Giang', '000827826195', '0877865245', 'Bắc Giang', 'pkl@gmail.com', 'Độc thân', 'Kinh', 'TS001', '2005-10-10', 'Bắc Giang', '', '', 'Image_Profile_MNV04'),
('MNV05', 'TP', 'MPB02', 900000, 'Nam', 'MHD05', 'Hoàng Anh Khoa', '2004-10-01', 'Đan Phượng - Hà Nội', '001297385197', '0877265456', 'Đan Phượng - Hà Nội', 'khoaha@gmail.com', 'Độc thân', 'Kinh', 'SV001', '2020-03-03', 'Đan Phượng', '', '', 'none_image_profile'),
('MNV06', 'NV', 'MPB03', 1500000, 'Nam', 'MHD06', 'Đặng Minh Khôi', '2004-05-05', 'Hoài Đức - Hà Nội', '123456789', '0556276648', 'Hoài Đức - Hà Nội', 'khoidm@gmail.com', 'Độc thân', 'Kinh', 'SV001', '2020-08-09', 'Hoài Đức', '', '', 'none_image_profile'),
('MNV07', 'NV', 'MPB03', 0.15, 'Nữ', 'MHD07', 'Trần Minh Khôi', '2004-08-05', '', '123456789', '0655745341', 'Ha Noi', 'khoi1@gmail.com', 'Độc thân', 'Kinh', 'SV002', NULL, NULL, '', '', 'none_image_profile'),
('MNV08', 'NV', 'MPB02', 700000, 'Nữ', 'MHD08', 'Nguyễn Minh Khôi', '2004-09-09', '', '123456789', '0877567893', 'Hà Nội', 'khoi2@gmail.com', 'Độc thân', 'Kinh', 'SV002', '2019-05-03', 'Bắc Giang', '', '', 'none_image_profile'),
('MNV10', 'NV', 'MPB01', 20000000, 'Nam', 'HDMNV10', 'Lê Minh Khôi', '2004-12-12', 'Thôn Xuân Tân - Xuân Hưng - Thọ Xuân - Thanh Hoá  - Việt Nam', '001206064297', '0916578134', 'Hà Đông - Hà Nội', 'khoi@gmail.com', 'Độc thân', 'Kinh', 'SV002', '2020-03-18', 'Thọ Xuân', 'SV40101208765', '0118000001', 'none_image_profile'),
('MNV12', 'NV', 'MPB05', 1000000, 'Nam', 'HDMNV12', 'Trần Anh Khoa', '2024-02-14', 'Đồng Họa - Xã Vạn Hòa - Huyện Nông Cống - Thanh Hóa', '001234957163', '0945875315', 'Hà Đông - Hà Nội', 'khoa@gmail.com', 'Độc thân', 'Kinh', 'SV001', '2019-04-05', 'Thanh Hóa', 'SV401975831', '0118648251', 'none_image_profile'),
('MNV24', 'NV', 'MPB02', 950000, 'Nam', 'HDMNV24', 'Phan Quang Huy', '2004-07-07', 'Khánh Hòa', '1234965137', '0856865245', 'Ha Noi', 'huy@gmail.com', 'Đã kết hôn', 'Kinh', 'SV003', '2020-07-07', 'Khánh Hòa', 'SV401658965', '118046701', 'none_image_profile'),
('MNV36', 'NV', 'MPB03', 900000, 'Nam', 'HDMNV36', 'Nguyễn Quang Trung', '1000-11-30', 'Thái Bình', '1262596315', '0558466648', 'Ha Noi', 'trung@gmail.com', 'Độc thân', 'Kinh', 'None', '2020-07-07', 'Thái Bình', 'SV401658583', '118124001', 'none_image_profile'),
('MNV37', '', '', 0, 'Nữ', '', 'trangnt', '0000-00-00', '', '001215387111', '024525896', '', '', 'Độc thân', 'Kinh', 'None', '2025-09-17', 'None', '', '', 'Image_Profile_MNV37'),
('test001', 'TTS', 'MPB03', 0, 'Nữ', '', 'Nguyễn Kim Liên', '0000-00-00', '', '', '', '', '', 'Độc thân', 'Kinh', NULL, NULL, NULL, '', '', 'none_image_profile'),
('test002', 'TTS', 'MPB03', 0, 'Nữ', '', 'Hoàng Thanh Hằng', '0000-00-00', '', '', '', '', '', 'Độc thân', 'Kinh', NULL, NULL, NULL, '', '', 'none_image_profile');

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

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_phanquyenuser`
--

CREATE TABLE `qlnv_phanquyenuser` (
  `id_user` int(11) NOT NULL,
  `role_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_phanquyenuser`
--

INSERT INTO `qlnv_phanquyenuser` (`id_user`, `role_id`) VALUES
(1, 1),
(2, 3),
(5, 2),
(7, 3),
(8, 1),
(11, 3),
(14, 3),
(17, 3),
(18, 3);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_phongban`
--

CREATE TABLE `qlnv_phongban` (
  `MaPB` varchar(8) NOT NULL,
  `TenPB` varchar(50) NOT NULL,
  `diachi` varchar(50) DEFAULT NULL,
  `sodt` varchar(10) DEFAULT NULL,
  `MaTruongPhong` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_phongban`
--

INSERT INTO `qlnv_phongban` (`MaPB`, `TenPB`, `diachi`, `sodt`, `MaTruongPhong`) VALUES
('MPB01', 'Marketing', 'Thanh Xuân - Hà Nội', '096358469', ''),
('MPB02', 'Công nghệ thông tin', 'Hà Đông - Hà Nội', '096358465', 'MNV05'),
('MPB03', 'Kế toán', 'Hà Nội', '096358461', ''),
('MPB04', 'Kiểm toán', 'Hà Nội', '096358467', ''),
('MPB05', 'Hành chính', 'Hà Nội', '096358468', ''),
('PBGD', 'Quản lý', 'Học Viện Công Nghệ Bưu Chính Viễn Thông', '0978836792', 'MNV04');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_role`
--

CREATE TABLE `qlnv_role` (
  `role_id` int(11) NOT NULL,
  `role_name` varchar(20) NOT NULL,
  `role_folder` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_role`
--

INSERT INTO `qlnv_role` (`role_id`, `role_name`, `role_folder`) VALUES
(1, 'Admin', ''),
(2, 'Trưởng Phòng', 'tp/'),
(3, 'Nhân Viên', 'user/');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_thoigiancongtac`
--

CREATE TABLE `qlnv_thoigiancongtac` (
  `id` int(11) NOT NULL,
  `MaNV` varchar(8) NOT NULL,
  `MaCV` varchar(8) NOT NULL,
  `NgayNhanChuc` date NOT NULL DEFAULT current_timestamp(),
  `NgayKetThuc` date DEFAULT NULL,
  `DuongNhiem` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_thoigiancongtac`
--

INSERT INTO `qlnv_thoigiancongtac` (`id`, `MaNV`, `MaCV`, `NgayNhanChuc`, `NgayKetThuc`, `DuongNhiem`) VALUES
(1, 'MNN01', 'NV', '2024-12-13', NULL, 1),
(2, 'MNN01', 'TTS', '2024-11-01', '2024-12-13', 0),
(3, 'MNV01', 'TTS', '2024-10-01', NULL, 1),
(4, 'MNV02', 'TTS', '2024-11-02', NULL, 1),
(5, 'MNV03', 'TTS', '2024-11-02', NULL, 1),
(6, 'MNV04', 'GD', '2024-12-01', NULL, 1),
(7, 'MNV05', 'TTS', '2024-12-01', NULL, 1),
(8, 'MNV06', 'NV', '2024-10-04', NULL, 1),
(9, 'MNV07', 'NV', '2024-10-04', NULL, 1),
(10, 'MNV08', 'NV', '2024-10-10', NULL, 1),
(11, 'MNV10', 'NV', '2024-12-13', NULL, 1),
(12, 'MNV12', 'TTS', '2024-12-13', '2024-12-18', 0),
(13, 'MNV24', 'NV', '2024-12-18', NULL, 1),
(14, 'MNV36', 'NV', '2024-12-18', NULL, 1),
(15, 'MNV12', 'NV', '2024-12-18', NULL, 1),
(19, 'MNV00100', 'NV', '2025-04-16', NULL, 1),
(20, 'MNV00100', 'NV', '2025-04-16', NULL, 1),
(21, 'MNV0097', 'NV', '2025-04-16', NULL, 1),
(22, 'MNV0097', 'NV', '2025-04-16', NULL, 1);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_thuongphat`
--

CREATE TABLE `qlnv_thuongphat` (
  `id` int(11) NOT NULL,
  `MaNV` varchar(8) NOT NULL,
  `Loai` tinyint(1) DEFAULT 0,
  `LyDo` varchar(100) NOT NULL,
  `Tien` double NOT NULL,
  `Ngay` date NOT NULL,
  `GhiChu` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_thuongphat`
--

INSERT INTO `qlnv_thuongphat` (`id`, `MaNV`, `Loai`, `LyDo`, `Tien`, `Ngay`, `GhiChu`) VALUES
(3, 'MNV02', 0, 'Chăm chỉ làm việc tốt', 10000, '2024-12-18', 'Tốt'),
(5, 'MNV03', 1, 'nhân viên ưu tú', 10000, '2022-12-01', ':))'),
(6, 'MNV03', 0, ':))', 20000, '2022-12-02', ':))');

--
-- Bẫy `qlnv_thuongphat`
--
DELIMITER $$
CREATE TRIGGER `delete_thuongphat_luong` AFTER DELETE ON `qlnv_thuongphat` FOR EACH ROW BEGIN
    DECLARE sotienphat double;
    DECLARE luongchamcong double;
    DECLARE luongDuocNhan double;
    DECLARE sotienthuong double;
    
    SET luongchamcong = (SELECT l.LuongChamCong
                        FROM qlnv_luong l
                        WHERE l.Nam = YEAR(OLD.Ngay) 
                         AND l.Thang = MONTH(OLD.Ngay) 
                         AND l.MaNV = OLD.MaNV);
    
    SET sotienphat = (SELECT SUM(tp.Tien) 
                      FROM qlnv_thuongphat tp 
                      WHERE tp.MaNV = OLD.MaNV AND MONTH(tp.Ngay) = MONTH(OLD.Ngay)
                     AND YEAR(tp.Ngay) = YEAR(OLD.Ngay) AND tp.Loai = 1);
    
    IF sotienphat IS NULL THEN
    	SET sotienphat = 0;
     END IF;
    
  
    set sotienthuong = (SELECT SUM(tp.Tien) 
                      FROM qlnv_thuongphat tp 
                      WHERE tp.MaNV = OLD.MaNV AND MONTH(tp.Ngay) = MONTH(OLD.Ngay)
                     AND YEAR(tp.Ngay) = YEAR(OLD.Ngay) AND tp.Loai = 0);
                     
    IF sotienthuong IS NULL THEN
    	SET sotienthuong = 0;
     END IF;
    
    SET luongDuocNhan = ROUND(luongchamcong - sotienphat + sotienthuong, -3);
   
    UPDATE `qlnv_luong`
    SET `SoTienThuong` = sotienthuong, `SoTienPhat` = sotienphat, `TongSoTien` = luongDuocNhan
    WHERE Nam = YEAR(OLD.Ngay) AND Thang = MONTH(OLD.Ngay) AND MaNV = OLD.MaNV;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `insert_thuongphat_luong` AFTER INSERT ON `qlnv_thuongphat` FOR EACH ROW BEGIN
    DECLARE sotienphat double;
    DECLARE luongchamcong double;
    DECLARE luongDuocNhan double;
    DECLARE sotienthuong double;
    
    SET luongchamcong = (SELECT l.LuongChamCong
                        FROM qlnv_luong l
                        WHERE l.Nam = YEAR(NEW.Ngay) 
                         AND l.Thang = MONTH(NEW.Ngay) 
                         AND l.MaNV = NEW.MaNV);
    
    SET sotienphat = (SELECT SUM(tp.Tien) 
                      FROM qlnv_thuongphat tp 
                      WHERE tp.MaNV = NEW.MaNV AND MONTH(tp.Ngay) = MONTH(NEW.Ngay)
                     AND YEAR(tp.Ngay) = YEAR(NEW.Ngay) AND tp.Loai = 1);
    
    IF sotienphat IS NULL THEN
    	SET sotienphat = 0;
     END IF;
    
  
    set sotienthuong = (SELECT SUM(tp.Tien) 
                      FROM qlnv_thuongphat tp 
                      WHERE tp.MaNV = NEW.MaNV AND MONTH(tp.Ngay) = MONTH(NEW.Ngay)
                     AND YEAR(tp.Ngay) = YEAR(NEW.Ngay) AND tp.Loai = 0);
                     
    IF sotienthuong IS NULL THEN
    	SET sotienthuong = 0;
     END IF;
    
    SET luongDuocNhan = ROUND(luongchamcong - sotienphat + sotienthuong, -3);
   
    UPDATE `qlnv_luong`
    SET `SoTienThuong` = sotienthuong, `SoTienPhat` = sotienphat, `TongSoTien` = luongDuocNhan
    WHERE Nam = YEAR(NEW.Ngay) AND Thang = MONTH(NEW.Ngay) AND MaNV = NEW.MaNV;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `update_thuongphat_luong` AFTER UPDATE ON `qlnv_thuongphat` FOR EACH ROW BEGIN
    DECLARE sotienphat double;
    DECLARE luongchamcong double;
    DECLARE luongDuocNhan double;
    DECLARE sotienthuong double;
    
    SET luongchamcong = (SELECT l.LuongChamCong
                        FROM qlnv_luong l
                        WHERE l.Nam = YEAR(OLD.Ngay) 
                         AND l.Thang = MONTH(OLD.Ngay) 
                         AND l.MaNV = OLD.MaNV);
    
    SET sotienphat = (SELECT SUM(tp.Tien) 
                      FROM qlnv_thuongphat tp 
                      WHERE tp.MaNV = OLD.MaNV AND MONTH(tp.Ngay) = MONTH(OLD.Ngay)
                     AND YEAR(tp.Ngay) = YEAR(OLD.Ngay) AND tp.Loai = 1);
    
    IF sotienphat IS NULL THEN
    	SET sotienphat = 0;
     END IF;
    
  
    set sotienthuong = (SELECT SUM(tp.Tien) 
                      FROM qlnv_thuongphat tp 
                      WHERE tp.MaNV = OLD.MaNV AND MONTH(tp.Ngay) = MONTH(OLD.Ngay)
                     AND YEAR(tp.Ngay) = YEAR(OLD.Ngay) AND tp.Loai = 0);
                     
    IF sotienthuong IS NULL THEN
    	SET sotienthuong = 0;
     END IF;
    
    SET luongDuocNhan = ROUND(luongchamcong - sotienphat + sotienthuong, -3);
   
    UPDATE `qlnv_luong`
    SET `SoTienThuong` = sotienthuong, `SoTienPhat` = sotienphat, `TongSoTien` = luongDuocNhan
    WHERE Nam = YEAR(OLD.Ngay) AND Thang = MONTH(OLD.Ngay) AND MaNV = OLD.MaNV;
    
    SET luongchamcong = (SELECT l.LuongChamCong
                        FROM qlnv_luong l
                        WHERE l.Nam = YEAR(NEW.Ngay) 
                         AND l.Thang = MONTH(NEW.Ngay) 
                         AND l.MaNV = NEW.MaNV);
    
    SET sotienphat = (SELECT SUM(tp.Tien) 
                      FROM qlnv_thuongphat tp 
                      WHERE tp.MaNV = NEW.MaNV AND MONTH(tp.Ngay) = MONTH(NEW.Ngay)
                     AND YEAR(tp.Ngay) = YEAR(NEW.Ngay) AND tp.Loai = 1);
    
    IF sotienphat IS NULL THEN
    	SET sotienphat = 0;
     END IF;
    
  
    set sotienthuong = (SELECT SUM(tp.Tien) 
                      FROM qlnv_thuongphat tp 
                      WHERE tp.MaNV = NEW.MaNV AND MONTH(tp.Ngay) = MONTH(NEW.Ngay)
                     AND YEAR(tp.Ngay) = YEAR(NEW.Ngay) AND tp.Loai = 0);
                     
    IF sotienthuong IS NULL THEN
    	SET sotienthuong = 0;
     END IF;
    
    SET luongDuocNhan = ROUND(luongchamcong - sotienphat + sotienthuong, -3);
   
    UPDATE `qlnv_luong`
    SET `SoTienThuong` = sotienthuong, `SoTienPhat` = sotienphat, `TongSoTien` = luongDuocNhan
    WHERE Nam = YEAR(NEW.Ngay) AND Thang = MONTH(NEW.Ngay) AND MaNV = NEW.MaNV;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_trinhdohocvan`
--

CREATE TABLE `qlnv_trinhdohocvan` (
  `MATDHV` varchar(8) NOT NULL,
  `TenTDHV` varchar(50) NOT NULL,
  `ChuyenNganh` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_trinhdohocvan`
--

INSERT INTO `qlnv_trinhdohocvan` (`MATDHV`, `TenTDHV`, `ChuyenNganh`) VALUES
('SV001', 'Chưa tốt nghiệp', 'Khoa học dữ liệu'),
('SV002', 'Chưa tốt nghiệp', 'Hóa Dược'),
('SV003', 'Chưa tốt nghiệp', 'Vật Lý'),
('TNKHMTTT', 'Tốt Nghiệp', 'Khoa học máy tính và thông tin'),
('TS001', 'Thạc Sĩ', 'Khoa học dữ liệu');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `qlnv_user`
--

CREATE TABLE `qlnv_user` (
  `Id_user` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(32) NOT NULL,
  `tennguoidung` varchar(50) NOT NULL,
  `MaNhanVien` varchar(8) NOT NULL,
  `LastLogin` datetime DEFAULT NULL,
  `register` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `qlnv_user`
--

INSERT INTO `qlnv_user` (`Id_user`, `username`, `password`, `tennguoidung`, `MaNhanVien`, `LastLogin`, `register`) VALUES
(1, 'admin', '0192023a7bbd73250516f069df18b500', 'Administrator', 'MNV02', '2025-09-21 14:56:23', '2024-12-01 14:57:45'),
(2, 'namnm', '827ccb0eea8a706c4c34a16891f84e7b', 'Nguyễn Minh Nam', 'MNV02', '2024-12-25 21:12:41', '2024-12-01 14:57:59'),
(5, 'khoaha', '827ccb0eea8a706c4c34a16891f84e7b', 'Hoang Anh Khoa', 'MNV05', '2025-09-29 00:09:24', '2024-12-21 22:27:34'),
(7, 'doanhpv', '827ccb0eea8a706c4c34a16891f84e7b', 'Pham Van Doanh', 'MNV03', '2025-09-16 22:51:25', '2024-12-20 20:20:24'),
(8, 'pkl', '827ccb0eea8a706c4c34a16891f84e7b', 'Phùng Khánh Linh', 'MNV04', '2025-09-29 00:21:44', '2024-12-21 14:43:39'),
(11, 'tungtn', '827ccb0eea8a706c4c34a16891f84e7b', 'Nguyễn Thanh Tùng', 'MNV01', '2025-09-29 00:23:33', '2024-12-25 20:48:52');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `qlnv_chamcong`
--
ALTER TABLE `qlnv_chamcong`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `qlnv_chamcongngay`
--
ALTER TABLE `qlnv_chamcongngay`
  ADD PRIMARY KEY (`MaChamCong`);

--
-- Chỉ mục cho bảng `qlnv_chamcongthang`
--
ALTER TABLE `qlnv_chamcongthang`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `qlnv_chamcongtongketthang`
--
ALTER TABLE `qlnv_chamcongtongketthang`
  ADD PRIMARY KEY (`Id`);

--
-- Chỉ mục cho bảng `qlnv_chucvu`
--
ALTER TABLE `qlnv_chucvu`
  ADD PRIMARY KEY (`MaCV`);

--
-- Chỉ mục cho bảng `qlnv_congty`
--
ALTER TABLE `qlnv_congty`
  ADD PRIMARY KEY (`ID`);

--
-- Chỉ mục cho bảng `qlnv_hopdong`
--
ALTER TABLE `qlnv_hopdong`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `qlnv_imagedata`
--
ALTER TABLE `qlnv_imagedata`
  ADD PRIMARY KEY (`ID_image`);

--
-- Chỉ mục cho bảng `qlnv_luong`
--
ALTER TABLE `qlnv_luong`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `qlnv_nhanvien`
--
ALTER TABLE `qlnv_nhanvien`
  ADD PRIMARY KEY (`MaNhanVien`);

--
-- Chỉ mục cho bảng `qlnv_phanquyenuser`
--
ALTER TABLE `qlnv_phanquyenuser`
  ADD PRIMARY KEY (`id_user`,`role_id`);

--
-- Chỉ mục cho bảng `qlnv_phongban`
--
ALTER TABLE `qlnv_phongban`
  ADD PRIMARY KEY (`MaPB`);

--
-- Chỉ mục cho bảng `qlnv_thoigiancongtac`
--
ALTER TABLE `qlnv_thoigiancongtac`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `qlnv_thuongphat`
--
ALTER TABLE `qlnv_thuongphat`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `qlnv_trinhdohocvan`
--
ALTER TABLE `qlnv_trinhdohocvan`
  ADD PRIMARY KEY (`MATDHV`);

--
-- Chỉ mục cho bảng `qlnv_user`
--
ALTER TABLE `qlnv_user`
  ADD PRIMARY KEY (`Id_user`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `qlnv_chamcong`
--
ALTER TABLE `qlnv_chamcong`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=95;

--
-- AUTO_INCREMENT cho bảng `qlnv_chamcongngay`
--
ALTER TABLE `qlnv_chamcongngay`
  MODIFY `MaChamCong` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- AUTO_INCREMENT cho bảng `qlnv_chamcongthang`
--
ALTER TABLE `qlnv_chamcongthang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT cho bảng `qlnv_chamcongtongketthang`
--
ALTER TABLE `qlnv_chamcongtongketthang`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT cho bảng `qlnv_congty`
--
ALTER TABLE `qlnv_congty`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT cho bảng `qlnv_hopdong`
--
ALTER TABLE `qlnv_hopdong`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT cho bảng `qlnv_luong`
--
ALTER TABLE `qlnv_luong`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT cho bảng `qlnv_thoigiancongtac`
--
ALTER TABLE `qlnv_thoigiancongtac`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT cho bảng `qlnv_thuongphat`
--
ALTER TABLE `qlnv_thuongphat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT cho bảng `qlnv_user`
--
ALTER TABLE `qlnv_user`
  MODIFY `Id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
