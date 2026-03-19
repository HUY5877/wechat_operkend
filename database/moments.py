# -*- coding:utf-8 -*-

from models.base import Moments
from typing import List

async def publish_moment(user_id: int, content: str) -> Moments:
    """发布朋友圈"""
    return await Moments.create(user_id=user_id, content=content)

async def delete_moment(moment_id: int, user_id: int) -> bool:
    """删除朋友圈：逻辑删除"""
    updated_count = await Moments.filter(id=moment_id, user_id=user_id).update(is_deleted=1)
    return updated_count > 0

async def get_timeline(user_id: int, skip: int = 0, limit: int = 20) -> List[Moments]:
    """获取朋友圈时间线"""
    return await Moments.filter(
        is_deleted=0
    ).order_by("-created_at").offset(skip).limit(limit)
