CREATE DATABASE IF NOT EXISTS eggdb COLLATE = 'utf8_unicode_ci';

CREATE TABLE  `eggdb`.`badges` (
    `badge_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY ,
    `link` VARCHAR( 255 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL ,
    `name` VARCHAR( 32 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL ,
    `description` VARCHAR( 1000 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL ,
    `parent` INT UNSIGNED NOT NULL ,
    `type` ENUM(  'category',  'boolean' ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT  'boolean' ,
    INDEX `parent` (  `parent` ) ,
    INDEX `type` (  `type` )
) ENGINE = INNODB CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE  `eggdb`.`users` (
    `user_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY ,
    `first_name` VARCHAR( 255 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL ,
    `last_name` VARCHAR( 255 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL ,
    `email` VARCHAR( 255 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL
) ENGINE = INNODB CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE  `eggdb`.`badges_users` (
    `badge_id` BIGINT UNSIGNED NOT NULL ,
    `user_id` BIGINT UNSIGNED NOT NULL ,
    `value` TINYINT( 1 ) NOT NULL ,
    `description` VARCHAR( 1000 ) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL ,
    PRIMARY KEY (  `badge_id` ,  `user_id` ) ,
    INDEX `badge_id` (  `badge_id`  ) ,
    INDEX `user_id` (  `user_id`  ) ,
    INDEX `value` (  `value`  )
) ENGINE = INNODB CHARACTER SET utf8 COLLATE utf8_unicode_ci;