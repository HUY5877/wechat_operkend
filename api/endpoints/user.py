# -*- coding:utf-8 -*-
from database.user import create_user, get_user_by_account, get_user_by_id, update_user

async def register(data: dict):
    account = data.get("account")
    password = data.get("password")
    name = data.get("name")

    # 账号、密码、名称为必需参数
    if not account or not password or not name:
        return {"result": "fail", "user_id": "", "text": "账号、密码、名称不能为空"}

    if await get_user_by_account(account):
        return {"result": "fail", "user_id": "", "text": "账号重复"}

    # 未传的参数使用默认值：status 为空字符串，profile_picture_id 为 0
    status = data.get("status", "")
    profile_picture_id = int(data.get("profile_picture_id", 0) or 0)

    user = await create_user(
        account=account,
        password=password,
        name=name,
        status=status,
        profile_picture_id=profile_picture_id
    )
    return {"result": "success", "user_id": str(user.id), "text": ""}

async def login(data: dict):
    account = data.get("account")
    password = data.get("password")
    user = await get_user_by_account(account)
    if not user or user.password != password:
        return {"result": "fail", "user_id": "", "text": "账号或密码错误"}

    # 仅用 user_id 作为前端唯一验证，不返回 token
    return {
        "result": "success",
        "user_id": str(user.id),
        "text": ""
    }

async def query_friend_homepage(data: dict):
    user_id = data.get("user_id")
    user = await get_user_by_id(user_id)
    if not user:
        return {}
    return {
        "friend_id": str(user.id),
        "account": user.account,
        "name": user.name,
        "status": str(user.status),
        "profile_picture_id": str(user.profile_picture_id)
    }

async def query_personal_homepage(data: dict):
    user_id = data.get("user_id")
    user = await get_user_by_id(user_id)
    if not user:
        return {}
    return {
        "user_id": str(user.id),
        "account": user.account,
        "name": user.name,
        "status": str(user.status),
        "profile_picture_id": str(user.profile_picture_id)
    }

async def recompose_personal_homepage(data: dict):
    user_id = data.get("user_id")

    # 先查出当前用户信息，未填字段保留原值
    current_user = await get_user_by_id(user_id)
    if not current_user:
        return {"result": "fail", "user_id": str(user_id), "text": "ID不存在"}

    update_data = {
        "name": data.get("name") if data.get("name") is not None else current_user.name,
        "status": data.get("status") if data.get("status") is not None else current_user.status,
        "profile_picture_id": int(data.get("profile_picture_id")) if data.get("profile_picture_id") is not None else current_user.profile_picture_id,
    }

    success_update = await update_user(user_id, **update_data)
    if success_update:
        return {"result": "success", "user_id": str(user_id), "text": ""}
    return {"result": "fail", "user_id": str(user_id), "text": "更新失败"}
