# -*- coding:utf-8 -*-
from database.contacts import add_contact, get_contacts, remove_contact
from database.user import get_user_by_account
from models.base import User, Contacts

async def add_friend(data: dict):
    user_id = data.get("user_id")
    account = data.get("account")

    # 查找好友是否存在
    friend_user = await get_user_by_account(account)
    if not friend_user:
        return {"result": "fail", "text": "用户不存在"}

    # 不能添加自己
    if str(friend_user.id) == str(user_id):
        return {"result": "fail", "text": "不能添加自己为好友"}

    # 检查是否已是好友
    existing = await Contacts.filter(user_id=user_id, friend_id=friend_user.id).exists()
    if existing:
        return {"result": "fail", "text": "已拥有好友"}

    await add_contact(user_id, friend_user.id)
    return {"result": "success", "text": ""}

async def query_contacts(data: dict):
    user_id = data.get("user_id")
    clist = await get_contacts(user_id)
    result = []
    for c in clist:
        f = await User.get_or_none(id=c.friend_id)
        result.append({
            "friend_id": str(c.friend_id),
            "name": f.name if f else "Unknown"
        })
    return {str(user_id): result}

async def query_contacts_search(data: dict):
    user_id = data.get("user_id")
    friend_name = data.get("friend_name", "")
    clist = await get_contacts(user_id)
    result = []
    for c in clist:
        f = await User.get_or_none(id=c.friend_id)
        # friend_name 为空时返回全部好友，否则模糊匹配名称
        if f and (not friend_name or friend_name in f.name):
            result.append({
                "friend_id": str(c.friend_id),
                "friend_name": f.name
            })
    return {str(user_id): result}
