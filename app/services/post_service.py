from typing import Optional, Dict, Any, List
from ..db import get_db
from ..exceptions import NotFound, BadRequest

def create_post(user_id: int, title, content) -> Dict[str, Any]:
    db = get_db()
    cur = db.execute(
        "INSERT INTO posts (user_id, title, content) VALUES(?, ?, ?)",
        (user_id, title, content)
    )
    db.commit()
    post_id = cur.lastrowid

    return {"id": post_id, "title": title}

def list_posts_paginated(user_id, page, page_size, keyword, sort, order):
    db = get_db()

    offset = (page - 1) * page_size

    where_clause = "WHERE user_id = ?"
    params = [user_id]

    if keyword:
        where_clause += " AND title LIKE ?"
        params.append(f"%{keyword}%")

    total_row = db.execute(
        f"SELECT COUNT(*) as count FROM posts {where_clause}",
        tuple(params)
    ).fetchone()

    total = total_row["count"]

    query = (
        f"SELECT id, title, content, created_at "
        f"FROM posts {where_clause} "
        f"ORDER BY {sort} {order} "
        f"LIMIT ? OFFSET ?"
    )

    rows = db.execute(
        query,
        tuple(params + [page_size, offset])
    ).fetchall()

    items = [dict(r) for r in rows]

    total_pages = (total + page_size - 1) // page_size

    return {
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages
        }
    }

def get_post(post_id: int, user_id: int) ->Optional[Dict[str, Any]]:
    db = get_db()
    row = db.execute(
        "SELECT id, title, content, created_at FROM posts WHERE id = ? AND user_id = ?",
        (post_id, user_id)
    ).fetchone()

    if not row:
        raise NotFound(code="POST_NOT_FOUND", message="Post not found")

    return dict(row)

def patch_post(
        post_id: int,
        user_id: int,
        title: Optional[str],
        content: Optional[str]
    ) -> Dict[str, Any]:
    updates = []
    params = []

    if title is not None:
        updates.append("title = ?")
        params.append(title)

    if content is not None:
        updates.append("content = ?")
        params.append(content)

    if not updates:
        raise BadRequest(message="no fields to update")

    params.extend([post_id, user_id])

    db = get_db()
    cur = db.execute(
        f"UPDATE posts SET {', '.join(updates)} WHERE id = ? AND user_id = ?",
        tuple(params)
    )
    db.commit()
    if cur.rowcount == 0:
        raise NotFound(code="POST_NOT_FOUND", message="post not found")


    return get_post(post_id=post_id, user_id=user_id)

def delete_post(post_id: int, user_id: int) -> bool:
    db = get_db()
    cur = db.execute(
        "DELETE FROM posts WHERE id = ? AND user_id = ?",
        (post_id, user_id)
    )
    db.commit()
    if cur.rowcount == 0:
        raise NotFound(code="POST_NOT_FOUND", message="post not found")
