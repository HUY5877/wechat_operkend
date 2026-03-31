# -*- coding:utf-8 -*-
import asyncio
import requests
from database.messages import send_message, get_messages, delete_message
from database.contacts import get_contacts
from models.base import Message, User
from tortoise.expressions import Q

async def add_message(data: dict):
    user_id = data.get("user_id")
    friend_id = data.get("friend_id")
    content = data.get("content")
    if not content:
        return {"result": "fail", "user_id": str(user_id), "text": "无文本"}
    await send_message(user_id, friend_id, content)
    quit()
    if str(friend_id) == "0":
        # 获取与该朋友的所有消息
        history = await get_messages(user_id, friend_id)
        # 历史记录是按时间倒序排列的，需要反转为正序供 LLM 使用
        history.reverse()
        
        messages_payload = []
        for msg in history:
            # 如果是当前用户发的消息，角色为 user；否则为 assistant
            role = "user" if str(msg.user_id) == str(friend_id) else "assistant"
            messages_payload.append({"role": role, "content": msg.content})
            
        async def fetch_llm():
            import os
            from openai import OpenAI

            client = OpenAI(
                # api_key=os.environ.get('DEEPSEEK_API_KEY'),
                api_key="sk-ca07c1345b034bd59c4b7a3408952d7e",
                base_url="https://api.deepseek.com")

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages_payload,
                stream=False
            )

            print(response.choices[0].message.content, 222222)
        
            # 将 LLM 的回复写入数据库，作为 friend_id 发送给 user_id
            await send_message(friend_id, user_id, response.choices[0].message.content)
        await fetch_llm()

    return {"result": "success", "user_id": str(user_id), "text": ""}

async def query_message_list(data: dict):
    """
    消息列表：与当前用户有消息往来的所有联系人及最新一条消息。
    已被当前用户删除的消息不计入。
    """
    user_id = data.get("user_id")
    # 查询该用户发出且自己未删除的消息 + 收到且自己未删除的消息
    sent = await Message.filter(user_id=user_id, is_deleted_sender=0).order_by("created_at").all()
    received = await Message.filter(friend_id=user_id, is_deleted_receiver=0).order_by("created_at").all()

    friends = {}
    all_msgs = sorted(list(sent) + list(received), key=lambda m: m.created_at)

    for m in all_msgs:
        other_id = m.friend_id if str(m.user_id) == str(user_id) else m.user_id
        key = str(other_id)
        if key not in friends:
            other_user = await User.get_or_none(id=other_id)
            friends[key] = {
                "user_id": str(other_id),
                "user_name": other_user.name if other_user else "Unknown",
                "new_message": m.content
            }
    return {str(user_id): list(friends.values())}

async def query_message(data: dict):
    """消息记录：查询用户与朋友双向消息，各自过滤自己已删的"""
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
    """
    删除消息：允许发送方或接收方逻辑删除，仅对自己隐藏。
    """
    user_id = data.get("user_id")
    message_id = data.get("message_id")
    success_del = await delete_message(message_id, user_id)
    if success_del:
        return {"result": "success", "user_id": str(user_id), "text": ""}
    return {"result": "fail", "user_id": str(user_id), "text": "消息不存在或无权限删除"}

async def search_message(data: dict):
    """
    查找消息：模糊查询，范围为用户与所有好友之间的对话（双向），
    过滤掉当前用户已删除的消息。
    """
    user_id = data.get("user_id")
    content = data.get("content", "")

    # 自己发出且未删除的
    sent = await Message.filter(
        user_id=user_id, is_deleted_sender=0, content__icontains=content
    ).all()
    # 自己收到且未删除的
    received = await Message.filter(
        friend_id=user_id, is_deleted_receiver=0, content__icontains=content
    ).all()

    result = []
    for m in sent:
        result.append({
            "friend_id": str(m.friend_id),
            "message_id": str(m.id),
            "content": m.content
        })
    for m in received:
        result.append({
            "friend_id": str(m.user_id),
            "message_id": str(m.id),
            "content": m.content
        })
    return {str(user_id): result}
