# -*- coding:utf-8 -*-
from datetime import timedelta, datetime
import jwt
from fastapi import HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette import status
from config import settings
from models.base import User

OAuth2 = OAuth2PasswordBearer(settings.SWAGGER_UI_OAUTH2_REDIRECT_URL)

def create_access_token(data: dict):
    token_data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data.update({"exp": expire})
    jwt_token = jwt.encode(token_data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return jwt_token

async def check_permissions(req: Request, token=Depends(OAuth2)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload:
            user_id = payload.get("user_id", None)
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except (PyJWTError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalid or expired")

    check_user = await User.get_or_none(id=user_id)
    if not check_user or check_user.status != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")

    req.state.user_id = user_id
