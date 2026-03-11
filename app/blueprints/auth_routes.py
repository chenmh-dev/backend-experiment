from flask import Blueprint, request
from ..utils import ok
from ..services import auth_service
from ..validators import get_json, required_str

bp = Blueprint("auth", __name__)

@bp.post("/login")
def login():
    data = get_json(request)

    username = required_str(data, "username", min_len=1, max_len=15)
    password = required_str(data, "password", min_len=3, max_len=25)

    result = auth_service.login(username, password)
    return ok(
        data={
            "user_id": result["user_id"], 
            "token": result["token"]
            },
        message="Login success",
        status=200
    )

@bp.post("/register")
def register():
    data = get_json(request)
    username = required_str(data, "username", min_len=1, max_len=15)
    password = required_str(data, "password", min_len=3, max_len=25)

    result = auth_service.register(username, password)

    return ok(
        data={"user_id": result["user_id"], "username": result["username"]}, 
        message="Register success", 
        status=201
    )

