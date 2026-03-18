# -*- coding:utf-8 -*-
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CreateUser(BaseModel):
    account: str
    password: str
    name: Optional[str] = None
    status: Optional[int] = 1

class UpdateUser(BaseModel):
    id: int
    account: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    status: Optional[int] = None

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account: str
    name: Optional[str] = None
    status: int
    created_at: datetime
    updated_at: datetime

class UserLogin(BaseModel):
    account: str
    password: str
