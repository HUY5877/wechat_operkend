# -*- coding:utf-8 -*-
from database.user import create_user, get_user_by_account, get_user_by_id, update_user
from core.Response import success, fail
from core.Auth import create_access_token
from config import settings

async def register(data: dict):
    account = data.get("account")
    password = data.get("password")
    name = data.get("name")
    if not account or not password:
        return {"result": "fail", "user_id": "", "text": "账号密码不能为空"}
    
    if await get_user_by_account(account):
        return {"result": "fail", "user_id": "", "text": "账号重复"}
    
    user = await create_user(account=account, password=password, name=name)
    return {"result": "success", "user_id": str(user.id), "text": ""}

async def login(data: dict):
    account = data.get("account")
    password = data.get("password")
    user = await get_user_by_account(account)
    if not user or user.password != password:
        return {"result": "fail", "user_id": "", "text": "账号或密码错误"}
    
    jwt_data = {"user_id": user.id}
    token = create_access_token(data=jwt_data)
    return {
        "result": "success", 
        "user_id": str(user.id), 
        "text": "",
        "token": token # Added for actual usability
    }

async def query_friend_homepage(data: dict):
    user_id = data.get("user_id")
    user = await get_user_by_id(user_id)
    if not user: return {}
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
    if not user: return {}
    return {
        "user_id": str(user.id),
        "account": user.account,
        "name": user.name,
        "status": str(user.status),
        "profile_picture_id": str(user.profile_picture_id)
    }

async def recompose_personal_homepage(data: dict):
    user_id = data.get("user_id")
    update_data = {
        "name": data.get("name"),
        "status": data.get("status"),
        "profile_picture_id": data.get("profile_picture_id")
    }
    # Remove None values
    update_data = {k: v for k, v in update_data.items() if v is not None}
    success_update = await update_user(user_id, **update_data)
    if success_update:
        return {"result": "success", "user_id": str(user_id), "text": ""}
    return {"result": "fail", "user_id": str(user_id), "text": "ID不存在或其他错误"}
