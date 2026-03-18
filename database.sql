-- 创建数据库
CREATE DATABASE IF NOT EXISTS `Wechat_HarmonyOS_main` DEFAULT CHARSET=utf8mb4;

-- 使用数据库
USE `Wechat_HarmonyOS_main`;

-- ======================
-- 用户表
-- ======================
CREATE TABLE user (
                      id BIGINT AUTO_INCREMENT UNIQUE,
                      account VARCHAR(50) NOT NULL UNIQUE,
                      password VARCHAR(255) NOT NULL,
                      name VARCHAR(50),
                      status TINYINT DEFAULT 1,
                      profile_picture_id BIGINT,
                      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ======================
-- 通讯录表
-- ======================
CREATE TABLE contacts (
                          id BIGINT AUTO_INCREMENT UNIQUE,
                          user_id BIGINT NOT NULL,
                          friend_id BIGINT NOT NULL,
                          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

                          UNIQUE KEY uk_user_friend (user_id, friend_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ======================
-- 消息表
-- ======================
CREATE TABLE message (
                         id BIGINT AUTO_INCREMENT UNIQUE,
                         user_id BIGINT NOT NULL,
                         friend_id BIGINT NOT NULL,
                         content TEXT,
                         created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                         is_deleted TINYINT DEFAULT 0,

                         INDEX idx_user_friend (user_id, friend_id),
                         INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ======================
-- 收藏表
-- ======================
CREATE TABLE favorites (
                           id BIGINT AUTO_INCREMENT UNIQUE,
                           user_id BIGINT NOT NULL,
                           message_id BIGINT NOT NULL,
                           created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                           is_deleted TINYINT DEFAULT 0,

                           UNIQUE KEY uk_user_message (user_id, message_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ======================
-- 朋友圈表
-- ======================
CREATE TABLE moments (
                         id BIGINT AUTO_INCREMENT UNIQUE,
                         user_id BIGINT NOT NULL,
                         content TEXT,
                         created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                         is_deleted TINYINT DEFAULT 0,

                         INDEX idx_user_id (user_id),
                         INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;