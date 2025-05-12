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

 Date: 06/05/2025 21:40:49
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for students_info
-- ----------------------------
DROP TABLE IF EXISTS `students_info`;
CREATE TABLE `students_info` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `StuNum` varchar(255) DEFAULT NULL,
  `StuName` varchar(255) DEFAULT NULL,
  `StuAge` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of students_info
-- ----------------------------
BEGIN;
INSERT INTO `students_info` (`id`, `StuNum`, `StuName`, `StuAge`) VALUES (1, '2022001', '张三', '14');
INSERT INTO `students_info` (`id`, `StuNum`, `StuName`, `StuAge`) VALUES (2, '2022002', '李四', '13');
INSERT INTO `students_info` (`id`, `StuNum`, `StuName`, `StuAge`) VALUES (3, '2022003', '钱五', '12');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
