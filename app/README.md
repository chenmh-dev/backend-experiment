# Backend Experiment

这个项目是一个内容系统 API，我重点设计了工程结构，比如 route/service 分层、统一异常体系、分页过滤 API 设计以及 request_id 日志追踪。

本项目的目标不是做功能完整的产品，而是搭建一个 **真实可运行、可扩展、结构清晰的后端架构基础**。

---

# Tech Stack

- Python 3.13
- Flask
- SQLite
- itsdangerous (Token 签名)
- Werkzeug password hashing

---

# Project Goals

本项目验证以下工程能力：

- 工厂模式 (create_app)
- Blueprint 模块化
- route / service 分层
- token 鉴权
- 资源级权限控制
- 统一返回结构
- 异常驱动错误体系
- request 级数据库生命周期
- 参数校验集中化
- 分页 / 过滤 / 排序 API 设计
- 请求日志与 request_id 追踪
- 配置分层（development / production）

---

# Project Structure


backend_experiment/
│
├── run.py
│
└── app/
├── init.py
├── config.py
├── db.py
├── auth.py
├── decorators.py
├── errors.py
├── exceptions.py
├── validators.py
├── utils.py
├── logging_utils.py
│
├── blueprints/
│ ├── auth_routes.py
│ ├── posts_routes.py
│ ├── user_routes.py
│ └── debug_routes.py
│
└── services/
├── auth_service.py
└── post_service.py


---

# Run the Project

## Development

PowerShell:

```powershell
$env:APP_ENV="development"
$env:SECRET_KEY="dev-secret-change-me"
python run.py

Server will start at:

http://127.0.0.1:5000
Production
$env:APP_ENV="production"
$env:SECRET_KEY="replace-with-strong-secret"
python run.py
API Overview
Auth
Register
POST /register

Body

{
  "username": "user",
  "password": "123"
}
Login
POST /login

Returns token.

{
  "success": true,
  "data": {
    "user_id": 1,
    "token": "xxxxx"
  }
}
User
Get current user
GET /me

Header

Authorization: Bearer <token>
Posts
Create post
POST /posts
List posts

Supports pagination, filtering and sorting.

GET /posts?page=1&page_size=10
GET /posts?keyword=flask
GET /posts?sort=id&order=desc
Get post
GET /posts/<id>
Update post
PATCH /posts/<id>
Delete post
DELETE /posts/<id>
Error Handling

All errors follow a unified structure.

{
  "success": false,
  "error": {
    "code": "POST_NOT_FOUND",
    "message": "post not found"
  }
}

Errors are implemented using an exception-driven architecture.

Logging

Every request generates a request_id.

Example response header:

X-Request-Id: 9fa2c1a8e2f3

Logs include:

request_id

HTTP method

path

response status

request duration

user_id

This enables request-level tracing during debugging.

Security Design

Token payload only contains user_id

All permissions validated via database

No trust in token payload beyond identity

SQL sorting uses whitelist to prevent injection

Development Notes

Debug endpoints are available only in development environment.

Example:

GET /debug/users

Not registered in production mode.

Future Extensions

Possible next steps:

Comments system

Role-based access control

Refresh token

PostgreSQL migration

SQLAlchemy ORM

OpenAPI / Swagger documentation