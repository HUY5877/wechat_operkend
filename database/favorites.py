# -*- coding:utf-8 -*-

from models.base import Favorites
from typing import List

async def add_favorite(user_id: int, message_id: int) -> Favorites:
    """添加收藏"""
    favorite, _ = await Favorites.get_or_create(user_id=user_id, message_id=message_id)
    return favorite

async def remove_favorite(user_id: int, message_id: int) -> bool:
    """移除收藏"""
    deleted_count = await Favorites.filter(user_id=user_id, message_id=message_id).delete()
    return deleted_count > 0

async def get_favorites(user_id: int, skip: int = 0, limit: int = 50) -> List[Favorites]:
    """获取收藏列表"""
    return await Favorites.filter(user_id=user_id, is_deleted=0).order_by("-created_at").offset(skip).limit(limit)
