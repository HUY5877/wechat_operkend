# -*- coding:utf-8 -*-

from models.base import Message
from typing import List
from tortoise.expressions import Q

async def send_message(user_id: int, friend_id: int, content: str) -> Message:
    """发送消息"""
    return await Message.create(user_id=user_id, friend_id=friend_id, content=content)

async def delete_message(message_id: int, current_user_id: int) -> bool:
    """
    删除消息：逻辑删除，只对当前用户隐藏。
    - 若当前用户是发送方（user_id），设置 is_deleted_sender=1
    - 若当前用户是接收方（friend_id），设置 is_deleted_receiver=1
    """
    msg = await Message.get_or_none(id=message_id)
    if not msg:
        return False

    if str(msg.user_id) == str(current_user_id):
        # 当前用户是发送方
        await Message.filter(id=message_id).update(is_deleted_sender=1)
        return True
    elif str(msg.friend_id) == str(current_user_id):
        # 当前用户是接收方
        await Message.filter(id=message_id).update(is_deleted_receiver=1)
        return True
    return False

async def get_messages(user_id: int, friend_id: int, skip: int = 0, limit: int = 50) -> List[Message]:
    """
    获取聊天记录（双向），各自隐藏已被自己删除的消息：
    - user_id 发送给 friend_id 的消息：对 user_id 隐藏 is_deleted_sender=1 的
    - friend_id 发送给 user_id 的消息：对 user_id 隐藏 is_deleted_receiver=1 的
    """
    # user 发的且 user 未删除的消息
    sent = await Message.filter(
        user_id=user_id, friend_id=friend_id, is_deleted_sender=0
    ).order_by("created_at").offset(skip).limit(limit)

    # friend 发的且 user（接收方）未删除的消息
    received = await Message.filter(
        user_id=friend_id, friend_id=user_id, is_deleted_receiver=0
    ).order_by("created_at").offset(skip).limit(limit)

    # 合并并按时间排序
    combined = list(sent) + list(received)
    combined.sort(key=lambda m: m.created_at)
    return combined
