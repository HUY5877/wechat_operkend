# -*- coding:utf-8 -*-
from database.moments import publish_moment, delete_moment, get_timeline

async def add_moments(data: dict):
    user_id = data.get("user_id")
    content = data.get("content")
    await publish_moment(user_id, content)
    return {"result": "success", "user_id": str(user_id), "text": ""}

async def query_moments(data: dict):
    user_id = data.get("user_id")
    mlist = await get_timeline(user_id)
    result = []
    for m in mlist:
        result.append({
            "moments_id": str(m.id),
            "moments_user_id": str(m.user_id),
            "moments_content": m.content,
            "created_at": m.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return {str(user_id): result}

async def delete_moments(data: dict):
    user_id = data.get("user_id")
    moments_id = data.get("moments_id")
    success_del = await delete_moment(moments_id, user_id)
    if success_del:
        return {"result": "success", "user_id": str(user_id), "text": ""}
    return {"result": "fail", "user_id": str(user_id), "text": "ID不存在"}
