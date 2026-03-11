from ..db import get_db
from typing import Dict, Any
from werkzeug.security import check_password_hash, generate_password_hash
from ..exceptions import UserExists, LoginFailed
from ..auth import generate_auth_token
import sqlite3

def login(username: str, password: str) -> Dict[str, Any]:
    db = get_db()
    cur = db.cursor()
    row = cur.execute(
        "SELECT id, username, password FROM users WHERE username = ?",
        (username,)#后面跟着逗号表示这是一个单元素元组，不是多余逗号
    ).fetchone()
    
    if row is None:
        raise LoginFailed()

    if not check_password_hash(row["password"], password):
        raise LoginFailed()
    user_id = row["id"]
    token = generate_auth_token({"user_id": user_id})

    return {"user_id": user_id, "token": token}

def register(username: str, password: str) -> Dict[str, Any]:
    db = get_db()
    hashed = generate_password_hash(password)
    try:
        cur = db.cursor()
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
            )
        db.commit()
    except sqlite3.IntegrityError:
        raise UserExists()
    
    return {"user_id": cur.lastrowid, "username": username}
    