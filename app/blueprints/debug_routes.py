from flask import Blueprint, current_app
from ..utils import ok, fail
from ..db import get_db

bp = Blueprint("debug", __name__)

@bp.get("/debug/users")
def debug_users():
    # 生产环境直接禁用
    if current_app.config.get("ENV_NAME") != "development":
        return fail(code="NOT_FOUND", message="Not Found", status=404)

    db = get_db()
    rows = db.execute("SELECT id, username FROM users ORDER BY id DESC").fetchall()

    data = [dict(r) for r in rows]
    return ok(data=data, message="users", status=200)