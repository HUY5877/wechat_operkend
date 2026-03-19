# FastAPI 基础架构模板项目

这是一个经过全面精简的标准且轻量级的 **FastAPI + Tortoise ORM** 示例项目。该项目已完全剥离复杂的微信集成、短信服务和多余的加密逻辑，并完美适配 Python 3.12 及 Pydantic v2。

## 项目结构说明

```text
wechat_operkend/
├── app.py                  # 项目的入口文件，负责初始化 FastAPI 实例、挂载路由、中间件以及跨域(CORS)和异常处理配置。
├── config.py               # 核心配置文件，使用 pydantic-settings 进行环境变量 (.env) 的加载和校验（例如 JWT 配置、数据库配置和服务器配置）。
├── requirement.txt         # 项目的环境依赖文件 (如 fastapi, tortoise-orm, PyJWT 等)。
├── database.sql            # 项目的数据库建表语句源码（定义了 user, contacts, message 等基础表）。
│
├── database/               # 数据库连接管理组件
│   └── mysql.py            # 配置 Tortoise ORM 引擎，包含了数据库地址、IP 及账号密码的加载。
│
├── models/                 # 数据库的 ORM 模型层 (Data Access)
│   └── base.py             # 包含了与 database.sql 中完全映射的数据库表模型（User, Contacts, Message, Favorites, Moments）。
│
├── schemas/                # Pydantic 数据验证模型层 (Data Transfer Objects)
│   └── user.py             # 用户相关的请求和响应结构体验证模型（包含创建、更新、返回以及登录的模型，已适配 Pydantic v2 的语法）。
│
├── api/                    # 所有的 API 端点与路由管理
│   ├── api.py              # 聚合所有子路由的主节点。
│   └── endpoints/          # 具体的业务处理 API 层。
│       └── user.py         # 用户的核心逻辑控制器 (Controller)。包含了注册、登录、修改信息、删除等标准化 CRUD 操作的样例。
│
├── core/                   # 核心通用功能与中间件
│   ├── Auth.py             # 简易而标准的 JWT 身份提取与验证。
│   ├── Events.py           # 管理 FastAPI 服务器启动和关闭时的生命周期钩子 (Lifecycle Hooks)。
│   ├── Exception.py        # 统一且全局的异常处理器 (捕捉错误并返回标准的 JSON)。
│   ├── Middleware.py       # 常规请求的基础中间件。
│   ├── Response.py         # 统一的响应结构体封装工厂（如 success(), fail() 返回统一的数据对象）。
│   ├── Router.py           # 合并 API 与 视图(View) 路由的文件。
│   └── Utils.py            # 工具箱函数。
│
├── views/                  # 后端模板渲染或视图层 (可选特性)
│   ├── viewpoints/         # 视图控制器。
│   └── views.py            # 视图主路由。
│
└── static/                 # 放置静态资源（如图片、css、js、Swagger 本地缓存等）和 Jinja2 模板。
```

## 环境配置手册

1. 进入项目根目录：
   ```bash
   cd C:\Users\1\Desktop\SUST\wechat_operkend # (将其替换为你的项目路径)
   ```
2. 创建并激活 Python 3.12 虚拟环境：
   ```bash
   conda create -n wechat python=3.12
   conda activate wechat
   ```
3. 升级 pip 并安装项目依赖：
   ```bash
   python.exe -m pip install --upgrade pip
   pip install -r requirement.txt
   ```
4. 环境变量配置：
   - 使用 pydantic-settings 加载 `.env` 文件。如果需要自定义配置，可以在根目录创建一个 `.env` 文件来覆盖 `config.py` 和 `database/mysql.py` 中的默认值（例如数据库连接：`BASE_HOST`, `BASE_USER`, `BASE_PASSWORD` 等）。
5. 启动后端项目：
   ```bash
   uvicorn app:app --reload
   ```

启动后，可以开始正常访问。