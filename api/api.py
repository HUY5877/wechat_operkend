# -*- coding:utf-8 -*-
from fastapi import APIRouter, Request
from api.endpoints import user, messages, contacts, moments, favorites

api_router = APIRouter(prefix="/api/v1")

@api_router.post("/service")
async def unified_service(request: Request):
    """
    统一服务入口点
    根据请求体中的 operation 和 table_name 分发逻辑
    """
    payload = await request.json()
    operation = payload.get("operation")
    table_name = payload.get("table_name")
    data = payload.get("data", {})

    # 分发逻辑
    if table_name == "user":
        if operation == "register":
            # 注册
            return await user.register(data)
        elif operation == "login":
            # 登录
            return await user.login(data)
        elif operation == "query_friend_homepage":

            return await user.query_friend_homepage(data)
        elif operation == "query_personal_homepage":
            # 个人主页
            return await user.query_personal_homepage(data)
        elif operation == "recompose_personal_homepage":
            return await user.recompose_personal_homepage(data)

    elif table_name == "message":
        if operation == "query_message_list":
            return await messages.query_message_list(data)
        elif operation == "query_message":
            return await messages.query_message(data)
        elif operation == "add_message":
            return await messages.add_message(data)
        elif operation == "delete_message":
            return await messages.delete_message_op(data)
        elif operation == "search_message":
            return await messages.search_message(data)

    elif table_name == "contacts":
        if operation == "query_contacts":
            return await contacts.query_contacts(data)
        elif operation == "add_friend":
            # 添加好友
            return await contacts.add_friend(data)
        elif operation == "query_contacts_":
            return await contacts.query_contacts_search(data)

    elif table_name == "moments":
        if operation == "query_moments":
            return await moments.query_moments(data)
        elif operation == "add_moments":
            return await moments.add_moments(data)
        elif operation == "delete_moments":
            return await moments.delete_moments(data)

    elif table_name == "favorites":
        if operation == "query_favorites":
            return await favorites.query_favorites(data)
        elif operation == "add_favorites_message":
            return await favorites.add_favorites_message(data)
        elif operation == "delete_favorites_message":
            return await favorites.delete_favorites_message(data)
        elif operation == "query_favorites_message":
            return await favorites.query_favorites_message(data)

    return {"result": "fail", "text": "无效的操作或表名"}
