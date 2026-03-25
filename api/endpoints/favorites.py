# -*- coding:utf-8 -*-
from database.favorites import add_favorite, remove_favorite, get_favorites
from database.contacts import get_contacts
from models.base import Message, Favorites

async def add_favorites_message(data: dict):
    """收藏消息：不同用户可以收藏同一条消息"""
    user_id = data.get("user_id")
    message_id = data.get("message_id")
    # 检查消息是否存在
    msg = await Message.get_or_none(id=message_id)
    if not msg:
        return {"result": "fail", "user_id": str(user_id), "text": "消息不存在"}
    # 检查当前用户是否已收藏（按 user_id + message_id 判断，不影响其他用户）
    already = await Favorites.filter(user_id=user_id, message_id=message_id, is_deleted=0).exists()
    if already:
        return {"result": "fail", "user_id": str(user_id), "text": "已经收藏"}
    await add_favorite(user_id, message_id)
    return {"result": "success", "user_id": str(user_id), "text": ""}

async def delete_favorites_message(data: dict):
    """删除收藏"""
    user_id = data.get("user_id")
    message_id = data.get("message_id")
    success_del = await remove_favorite(user_id, message_id)
    if success_del:
        return {"result": "success", "user_id": str(user_id), "text": ""}
    return {"result": "fail", "user_id": str(user_id), "text": "收藏不存在"}

async def query_favorites(data: dict):
    """收藏列表"""
    user_id = data.get("user_id")
    flist = await get_favorites(user_id)
    result = []
    for f in flist:
        msg = await Message.get_or_none(id=f.message_id)
        result.append({
            "favorites_id": str(f.id),
            "favorites_user_id": str(f.user_id),
            "content": msg.content if msg else "",
            "created_at": f.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return {str(user_id): result}

async def query_favorites_message(data: dict):
    """
    搜索收藏：模糊查询，范围为用户与所有好友之间的对话。
    若 content 为空，直接返回空列表（不做全量返回）。
    """
    user_id = data.get("user_id")
    content = data.get("content", "")

    # content 为空时直接返回空列表
    if not content:
        return {str(user_id): []}

    # 获取好友 ID 列表
    clist = await get_contacts(user_id)
    friend_ids = [c.friend_id for c in clist]

    flist = await get_favorites(user_id)
    result = []
    for f in flist:
        msg = await Message.get_or_none(id=f.message_id)
        if not msg:
            continue
        # 判断消息属于用户与好友之间的双向对话
        is_own_send = str(msg.user_id) == str(user_id) and msg.friend_id in friend_ids
        is_received = str(msg.friend_id) == str(user_id) and msg.user_id in friend_ids
        # 模糊匹配内容
        if (is_own_send or is_received) and content in msg.content:
            result.append({
                "favorites_id": str(f.id),
                "favorites_content": msg.content,
                "created_at": f.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
    return {str(user_id): result}