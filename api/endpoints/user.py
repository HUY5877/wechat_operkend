# -*- coding:utf-8 -*-
from fastapi import APIRouter, Depends, Request
from models.base import User
from schemas import user
from core.Response import success, fail
from core.Auth import check_permissions, create_access_token
from config import settings

router = APIRouter()

@router.post("/register", summary="User Registration")
async def register(post: user.CreateUser):
    get_user = await User.get_or_none(account=post.account)
    if get_user:
        return fail(msg=f"Account {post.account} already exists!")
    create_user = await User.create(**post.model_dump())
    if not create_user:
        return fail(msg="Registration failed")
    return success(msg="Registration successful")

@router.post("/login", summary="User Login")
async def login(post: user.UserLogin):
    get_user = await User.get_or_none(account=post.account)
    if not get_user or get_user.password != post.password:
        return fail(msg="Incorrect account or password")
    if get_user.status != 1:
        return fail(msg="Account inactive")
    
    jwt_data = {"user_id": get_user.id}
    jwt_token = create_access_token(data=jwt_data)
    data = {"token": jwt_token, "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60}
    return success(msg="Login successful", data=data)

@router.get("/info", summary="Get User Info", dependencies=[Depends(check_permissions)])
async def user_info(req: Request):
    user_data = await User.get_or_none(id=req.state.user_id)
    if not user_data:
        return fail(msg="User not found")
    return success(msg="User Info", data=user.UserResponse.model_validate(user_data).model_dump())

@router.put("/update", summary="Update User Info", dependencies=[Depends(check_permissions)])
async def update_user(req: Request, post: user.UpdateUser):
    if post.id != req.state.user_id:
        return fail(msg="Cannot update other users")
    data = post.model_dump(exclude_unset=True)
    data.pop("id", None)
    await User.filter(id=req.state.user_id).update(**data)
    return success(msg="Update successful")

@router.delete("/delete", summary="Delete User", dependencies=[Depends(check_permissions)])
async def delete_user(req: Request):
    await User.filter(id=req.state.user_id).delete()
    return success(msg="Delete successful")
