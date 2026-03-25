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
                      status VARCHAR(100) DEFAULT '',
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
                         is_deleted_sender TINYINT DEFAULT 0,
                         is_deleted_receiver TINYINT DEFAULT 0,

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










-- ======================
-- 迁移操作（对已有数据库执行）
-- ======================
USE `Wechat_HarmonyOS_main`;

-- 1. user 表：status 字段从 TINYINT 改为 VARCHAR(100)，支持字符串类型签名
ALTER TABLE user MODIFY COLUMN status VARCHAR(100) DEFAULT '';

-- 2. message 表：将单一 is_deleted 拆分为发送方/接收方独立软删除字段
ALTER TABLE message DROP COLUMN is_deleted;
ALTER TABLE message ADD COLUMN is_deleted_sender TINYINT DEFAULT 0 COMMENT '发送方逻辑删除，只对发送方隐藏';
ALTER TABLE message ADD COLUMN is_deleted_receiver TINYINT DEFAULT 0 COMMENT '接收方逻辑删除，只对接收方隐藏';