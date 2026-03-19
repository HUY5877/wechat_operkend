# -*- coding:utf-8 -*-
"""
@Created on : 2022/4/22 22:02
@Author: binkuolo
@Des: app运行时文件
"""

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from config import settings
from fastapi.staticfiles import StaticFiles
from core import Exception, Events, Router, Middleware
from fastapi.templating import Jinja2Templates
from tortoise.exceptions import OperationalError, DoesNotExist, IntegrityError, ValidationError
from fastapi.openapi.docs import (get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html)
from fastapi.openapi.utils import get_openapi

application = FastAPI(
    debug=settings.APP_DEBUG,
    swagger_ui_oauth2_redirect_url=settings.SWAGGER_UI_OAUTH2_REDIRECT_URL,
)



# 事件监听
application.add_event_handler("startup", Events.startup(application))
application.add_event_handler("shutdown", Events.stopping(application))

# 异常错误处理
application.add_exception_handler(HTTPException, Exception.http_error_handler)
application.add_exception_handler(RequestValidationError, Exception.http422_error_handler)
application.add_exception_handler(Exception.UnicornException, Exception.unicorn_exception_handler)
application.add_exception_handler(DoesNotExist, Exception.mysql_does_not_exist)
application.add_exception_handler(IntegrityError, Exception.mysql_integrity_error)
application.add_exception_handler(ValidationError, Exception.mysql_validation_error)
application.add_exception_handler(OperationalError, Exception.mysql_operational_error)


# 中间件
application.add_middleware(Middleware.BaseMiddleware)

application.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

application.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie=settings.SESSION_COOKIE,
    max_age=settings.SESSION_MAX_AGE
)

# 路由
application.include_router(Router.router)

# 静态资源目录
application.mount('/', StaticFiles(directory=settings.STATIC_DIR), name="static")
application.state.views = Jinja2Templates(directory=settings.TEMPLATE_DIR)

app = application
