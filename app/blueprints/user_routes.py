from flask import Blueprint, g
from ..decorators import require_auth_token
from ..db import get_db
from ..utils import fail, ok

bp = Blueprint("user", __name__)

@bp.route("/me")
@require_auth_token
def me():
    user_id = g.user["user_id"]

    db = get_db()
    cur = db.cursor()
    row = cur.execute(
        "SELECT id, username FROM users WHERE id = ?",
        (user_id, )
    ).fetchone()
    

    if not row:
        return fail(code="USER_NOT_FOUND", message="User not found", status=404)

    return ok(
        data={
            "id": row["id"], 
            "username": row["username"]
        }, 
        message="Me", 
        status=200
    )