# -*- coding:utf-8 -*-
from database.favorites import add_favorite, remove_favorite, get_favorites
from models.base import Message

async def add_favorites_message(data: dict):
    # 添加收藏
    user_id = data.get("user_id")
    message_id = data.get("message_id")
    # 检查消息是否存在
    msg = await Message.get_or_none(id=message_id)
    if not msg:
        return {"result": "fail", "user_id": str(user_id), "text": "消息不存在"}
    # 检查是否已收藏
    if await add_favorite(user_id, message_id):
        return {"result": "success", "user_id": str(user_id), "text": ""}
    return {"result": "fail", "user_id": str(user_id), "text": "已收藏"}

async def delete_favorites_message(data: dict):
    # 删除收藏
    user_id = data.get("user_id")
    message_id = data.get("message_id")
    success_del = await remove_favorite(user_id, message_id)
    if success_del:
        return {"result": "success", "user_id": str(user_id), "text": ""}
    return {"result": "fail", "user_id": str(user_id), "text": "收藏不存在"}

async def query_favorites(data: dict):
    # 查询收藏列表
    user_id = data.get("user_id")
    flist = await get_favorites(user_id)
    result = []
    for f in flist:
        msg = await Message.get_or_none(id=f.message_id)
        result.append({
            "favorites_id": str(f.id),
            "favorites_user_id": str(f.user_id),
            "content": msg.content if msg else "Original message deleted",
            "created_at": f.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return {str(user_id): result}

async def query_favorites_message(data: dict):
    # 查询收藏内容
    user_id = data.get("user_id")
    content = data.get("content")
    flist = await get_favorites(user_id)
    result = []
    for f in flist:
        msg = await Message.get_or_none(id=f.message_id)
        if msg and content in msg.content:
            result.append({
                "favorites_id": str(f.id),
                "favorites_content": msg.content,
                "created_at": f.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
    return {str(user_id): result}