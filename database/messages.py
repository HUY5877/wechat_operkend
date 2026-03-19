# -*- coding:utf-8 -*-

from models.base import Message
from typing import List
from tortoise.expressions import Q

async def send_message(user_id: int, friend_id: int, content: str) -> Message:
    """发送消息"""
    return await Message.create(user_id=user_id, friend_id=friend_id, content=content)

async def delete_message(message_id: int, user_id: int) -> bool:
    """删除(撤回)消息：逻辑删除"""
    updated_count = await Message.filter(id=message_id, user_id=user_id).update(is_deleted=1)
    return updated_count > 0

async def get_messages(user_id: int, friend_id: int, skip: int = 0, limit: int = 50) -> List[Message]:
    """获取聊天记录，双方均可见"""
    # 使用 Q 对象进行复杂的 OR 查询
    return await Message.filter(
        Q(user_id=user_id, friend_id=friend_id) | Q(user_id=friend_id, friend_id=user_id),
        is_deleted=0
    ).order_by("-created_at").offset(skip).limit(limit)
