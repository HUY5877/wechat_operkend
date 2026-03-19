# -*- coding:utf-8 -*-
from database.messages import send_message, get_messages, delete_message
from models.base import Message, User
from tortoise.expressions import Q

async def add_message(data: dict):
    user_id = data.get("user_id")
    friend_id = data.get("friend_id")
    content = data.get("content")
    if not content:
        return {"result": "fail", "user_id": str(user_id), "text": "无文本"}
    await send_message(user_id, friend_id, content)
    return {"result": "success", "user_id": str(user_id), "text": ""}

async def query_message_list(data: dict):
    user_id = data.get("user_id")
    # 获取与当前用户有过消息往来的所有朋友及其最后一条消息
    # 这是一个比较复杂的查询，这里做简易实现
    # 先找所有相关用户
    history = await Message.filter(Q(user_id=user_id) | Q(friend_id=user_id)).order_by("-created_at").all()
    friends = {}
    for m in history:
        other_id = m.friend_id if m.user_id == user_id else m.user_id
        if other_id not in friends:
            other_user = await User.get_or_none(id=other_id)
            friends[other_id] = {
                "user_id": str(other_id),
                "user_name": other_user.name if other_user else "Unknown",
                "new_message": m.content
            }
    return {str(user_id): list(friends.values())}

async def query_message(data: dict):
    user_id = data.get("user_id")
    friend_id = data.get("friend_id")
    msgs = await get_messages(user_id, friend_id)
    result = []
    for m in msgs:
        result.append({
            "message_id": str(m.id),
            "message_user_id": str(m.user_id),
            "content": m.content
        })
    return {str(user_id): result}

async def delete_message_op(data: dict):
    user_id = data.get("user_id")
    message_id = data.get("message_id")
    success_del = await delete_message(message_id, user_id)
    if success_del:
        return {"result": "success", "user_id": str(user_id), "text": ""}
    return {"result": "fail", "user_id": str(user_id), "text": "消息不存在"}

async def search_message(data: dict):
    user_id = data.get("user_id")
    content = data.get("content")
    msgs = await Message.filter(Q(user_id=user_id) | Q(friend_id=user_id), content__icontains=content, is_deleted=0).all()
    result = []
    for m in msgs:
        friend_id = m.friend_id if m.user_id == user_id else m.user_id
        result.append({
            "friend_id": str(friend_id),
            "message_id": str(m.id),
            "content": m.content
        })
    return {str(user_id): result}
