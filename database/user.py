# -*- coding:utf-8 -*-

from models.base import User
from typing import Optional, List

async def create_user(account: str, password: str, name: str, status: str = '', profile_picture_id: int = 0) -> User:
    """创建用户，account/password/name 为必需，其余默认"""
    return await User.create(
        account=account,
        password=password,
        name=name,
        status=status,
        profile_picture_id=profile_picture_id
    )

async def get_user_by_account(account: str) -> Optional[User]:
    """通过账号获取用户"""
    return await User.get_or_none(account=account)

async def get_user_by_id(user_id: int) -> Optional[User]:
    """通过ID获取用户"""
    return await User.get_or_none(id=user_id)

async def update_user(user_id: int, **kwargs) -> bool:
    """更新用户信息"""
    updated_count = await User.filter(id=user_id).update(**kwargs)
    return updated_count > 0

async def delete_user(user_id: int) -> bool:
    """删除用户"""
    deleted_count = await User.filter(id=user_id).delete()
    return deleted_count > 0
