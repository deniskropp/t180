CREATE DATABASE IF NOT EXISTS `db`; USE `db`; 
SET FOREIGN_KEY_CHECKS=0;
SET UNIQUE_CHECKS=0;
DROP TABLE IF EXISTS `aux`;
CREATE TABLE `aux` (
  `uuid` char(40) NOT NULL,
  `mimetype` char(40) NOT NULL,
  `data_uuid` char(40) NOT NULL,
  PRIMARY KEY (`uuid`,`mimetype`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;
DROP TABLE IF EXISTS `main`;
CREATE TABLE `main` (
  `uuid` char(40) NOT NULL,
  `added_time` double NOT NULL,
  `last_used_time` double,
  `mimetypes` text NOT NULL,
  `text` text,
  `starred` tinyint(1),
  PRIMARY KEY (`uuid`),
  CONSTRAINT `main_chk_bpmd53ir` CHECK ((`added_time` > 0)),
  CONSTRAINT `main_chk_01k9530r` CHECK ((`last_used_time` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;
DROP TABLE IF EXISTS `version`;
CREATE TABLE `version` (
  `db_version` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;
