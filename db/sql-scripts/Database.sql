##########################
# Annales Memum Database #
##########################
# Sam Pearce
# Version: 1.0

# Create Database
DROP DATABASE IF EXISTS `annales_memum`;
CREATE DATABASE `annales_memum` DEFAULT CHARSET utf8;
USE `annales_memum`;

# Create Users
DROP USER IF EXISTS 'ann_mem_user'@'localhost';
CREATE USER 'ann_mem_user'@'localhost' IDENTIFIED BY '4nn_m3m';
GRANT ALL PRIVILEGES ON `annales_memum`.* TO 'ann_mem_user'@'localhost';

DROP USER IF EXISTS 'ann_mem_user'@'%';
CREATE USER 'ann_mem_user'@'%' IDENTIFIED BY '4nn_m3m';
GRANT INSERT, SELECT, UPDATE, DELETE ON `annales_memum`.* TO 'ann_mem_user'@'%';

# Create Tables
DROP TABLE IF EXISTS tbl_user;
CREATE TABLE tbl_user (
	id_user INT NOT NULL UNIQUE AUTO_INCREMENT,
    username VARCHAR(64) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS tbl_tag;
CREATE TABLE tbl_tag (
	id_tag INT NOT NULL UNIQUE AUTO_INCREMENT,
    name VARCHAR(16) NOT NULL
);

DROP TABLE IF EXISTS tbl_page;
CREATE TABLE tbl_page (
	id_page INT NOT NULL UNIQUE AUTO_INCREMENT,
    creator_user_id INT NOT NULL,
	title VARCHAR(64) NOT NULL,
    text TEXT NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    
    FOREIGN KEY (creator_user_id)
	REFERENCES tbl_user(id_user)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

DROP TABLE IF EXISTS tbl_page_tags;
CREATE TABLE tbl_page_tags (
	id_page_tags INT NOT NULL UNIQUE AUTO_INCREMENT,
    page_id INT NOT NULL,
    tag_id INT NOT NULL,
    
    FOREIGN KEY (page_id)
	REFERENCES tbl_page(id_page)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    
    FOREIGN KEY (tag_id)
	REFERENCES tbl_tag(id_tag)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);
