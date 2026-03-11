import sqlite3
from typing import Dict, Any
from ..db import get_db
from ..exceptions import NotFound

def _ensure_post_exists(post_id: int):
    db = get_db()
    row = db.execute("SELECT id FROM COMMENTS WHERE post_id = ?", (post_id,)).fetchone()
    if not row:
        raise NotFound(code="POST_NOT_FOUND", message="Post not found")

def create_comment(user_id: int, post_id: int, content: str) -> Dict[str, Any]:
    _ensure_post_exists(post_id)

    db = get_db()
    cur = db.execute(
        "INSERT INTO comments (user_id, post_id, content) VALUES(?, ?, ?)",
        (user_id, post_id, content)
    )
    db.commit()

    comment_id = cur.lastrowid

    return {"id": comment_id, "post_id": post_id, "user_id": user_id, "content": content}

def list_comments(post_id: int):
    _ensure_post_exists(post_id)

    db = get_db()
    rows = db.execute(
        "SELECT id, user_id, content, created_at FROM comments WHERE post_id = ?",
        (post_id,)
    ).fetchall()

    return [dict(r) for r in rows]

def delete_comment(user_id: int, comment_id: int):
    db = get_db()
    cur = db.execute(
        "DELETE FROM comments WHERE id = ? AND user_id = ?",
        (comment_id, user_id)
    )
    db.commit()

    if cur.rowcount == 0:
        raise NotFound(code="COMMENT_NOT_FOUND", message="Comment not found") 