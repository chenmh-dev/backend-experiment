from flask import Blueprint, request, g
from ..decorators import require_auth_token
from ..utils import ok
from ..validators import (
    get_json, 
    required_str, 
    optional_str, 
    require_any, 
    parse_pagination,
    parse_sorting,
    parse_keyword
)
from ..services.post_service import(
    create_post,
    list_posts_paginated,
    get_post,
    patch_post,
    delete_post
)

bp = Blueprint("posts", __name__)

@bp.post("/posts")
@require_auth_token
def create_post_route():
    data = get_json(request)
    title = required_str(data, "title", min_len=1, max_len=100)
    content = required_str(data, "content", min_len=1, max_len=5000)
    user_id = g.user["user_id"]
    post = create_post(user_id=user_id, title=title, content=content)
    return ok(data=post, message="Post created", status=201)

@bp.get("/posts")
@require_auth_token
def list_posts_route():
    user_id = g.user["user_id"]

    page, page_size = parse_pagination(request)
    keyword = parse_keyword(request)
    sort, order = parse_sorting(
        request,
        allowed_fields=["id", "created_at", "title"],
        default_field="id"
    )
    data = list_posts_paginated(user_id, page, page_size, keyword, sort, order)

    return ok(data=data, message="Posts", status=200)

@bp.get("/posts/<int:post_id>")
@require_auth_token
def get_post_route(post_id: int):
    user_id = g.user["user_id"]
    post = get_post(post_id=post_id, user_id=user_id)
    return ok(data=post, message="Post", status=200)

@bp.patch("/posts/<int:post_id>")
@require_auth_token
def patch_post_route(post_id: int):
    data = get_json(request)
    title = optional_str(data, "title", min_len=1, max_len=100)
    content = optional_str(data, "content", min_len=1, max_len=5000)
    require_any(title, content)
    user_id = g.user["user_id"]
    update = patch_post(post_id=post_id, user_id=user_id, title=title, content=content)
    return ok(data=update,message="Post updated", status=200)

@bp.delete("/posts/<int:post_id>")
@require_auth_token
def delete_post_route(post_id: int):
    user_id = g.user["user_id"]
    delete_post(post_id=post_id, user_id=user_id)
    return ok(data={"deleted": True}, message="Post deleted", status=200)