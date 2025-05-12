/*
 Navicat Premium Dump SQL

 Source Server         : docker_mysql
 Source Server Type    : MySQL
 Source Server Version : 50741 (5.7.41)
 Source Host           : localhost:3306
 Source Schema         : NanGeAGI

 Target Server Type    : MySQL
 Target Server Version : 50741 (5.7.41)
 File Encoding         : 65001

 Date: 06/05/2025 21:40:56
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for students_score
-- ----------------------------
DROP TABLE IF EXISTS `students_score`;
CREATE TABLE `students_score` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `StuNum` varchar(255) DEFAULT NULL,
  `score` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of students_score
-- ----------------------------
BEGIN;
INSERT INTO `students_score` (`id`, `StuNum`, `score`) VALUES (1, '2022001', '89.3');
INSERT INTO `students_score` (`id`, `StuNum`, `score`) VALUES (2, '2022002', '99.4');
INSERT INTO `students_score` (`id`, `StuNum`, `score`) VALUES (3, '2022003', '39.3');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
