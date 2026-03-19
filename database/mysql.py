# -*- coding:utf-8 -*-
"""
@Time : 2022/4/24 10:15 AM
@Author: binkuolo
@Des: mysql数据库
"""

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import os


# -----------------------数据库配置-----------------------------------
DB_ORM_CONFIG = {
    "connections": {
        "base": {
            'engine': 'tortoise.backends.mysql',
            "credentials": {
                'host': os.getenv('BASE_HOST', '47.110.126.251'),
                'user': os.getenv('BASE_USER', 'root'),
                'password': os.getenv('BASE_PASSWORD', 'sust123456'),
                'port': int(os.getenv('BASE_PORT', 3306)),
                'database': os.getenv('BASE_DB', 'Wechat_HarmonyOS_main'),
            }
        },
    },
    "apps": {
        "base": {"models": ["models.base"], "default_connection": "base"},
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}


async def register_mysql(app: FastAPI):
    # 注册数据库
    register_tortoise(
        app,
        config=DB_ORM_CONFIG,
        generate_schemas=False,
        add_exception_handlers=False,
    )
