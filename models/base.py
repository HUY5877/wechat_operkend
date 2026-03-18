# -*- coding:utf-8 -*-
from tortoise import fields
from tortoise.models import Model

# ======================
# 用户表
# ======================
class User(Model):
    id = fields.BigIntField(pk=True, unique=True)
    account = fields.CharField(max_length=50, unique=True, null=False)
    password = fields.CharField(max_length=255, null=False)
    name = fields.CharField(max_length=50, null=True)
    status = fields.IntField(default=1) # TINYINT doesn't exist directly, IntField is fine
    profile_picture_id = fields.BigIntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "user"

# ======================
# 通讯录表
# ======================
class Contacts(Model):
    id = fields.BigIntField(pk=True, unique=True)
    user_id = fields.BigIntField(null=False)
    friend_id = fields.BigIntField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "contacts"
        unique_together = (("user_id", "friend_id"),)

# ======================
# 消息表
# ======================
class Message(Model):
    id = fields.BigIntField(pk=True, unique=True)
    user_id = fields.BigIntField(null=False)
    friend_id = fields.BigIntField(null=False)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    is_deleted = fields.IntField(default=0)

    class Meta:
        table = "message"
        indexes = (
            ("user_id", "friend_id"),
        )

# ======================
# 收藏表
# ======================
class Favorites(Model):
    id = fields.BigIntField(pk=True, unique=True)
    user_id = fields.BigIntField(null=False)
    message_id = fields.BigIntField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    is_deleted = fields.IntField(default=0)

    class Meta:
        table = "favorites"
        unique_together = (("user_id", "message_id"),)

# ======================
# 朋友圈表
# ======================
class Moments(Model):
    id = fields.BigIntField(pk=True, unique=True)
    user_id = fields.BigIntField(null=False, index=True)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    is_deleted = fields.IntField(default=0)

    class Meta:
        table = "moments"
