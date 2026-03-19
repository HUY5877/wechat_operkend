# -*- coding:utf-8 -*-

from models.base import Contacts
from typing import List

async def add_contact(user_id: int, friend_id: int) -> Contacts:
    """添加好友"""
    contact, _ = await Contacts.get_or_create(user_id=user_id, friend_id=friend_id)
    return contact

async def remove_contact(user_id: int, friend_id: int) -> bool:
    """删除好友"""
    deleted_count = await Contacts.filter(user_id=user_id, friend_id=friend_id).delete()
    return deleted_count > 0

async def get_contacts(user_id: int, skip: int = 0, limit: int = 100) -> List[Contacts]:
    """获取好友列表"""
    return await Contacts.filter(user_id=user_id).offset(skip).limit(limit)
