from flask import Blueprint, request, g
from ..decorators import require_auth_token
from ..validators import get_json, required_str
from ..services.comment_service import create_comment, list_comments, delete_comment
from ..utils import ok

bp = Blueprint("comments", __name__)

@bp.post("/posts/<int:post_id>/comments")
@require_auth_token
def post_comment_route(post_id: int):
    data = get_json(request)
    content = required_str(data, "content", min_len=1, max_len=1000)

    user_id = g.user["user_id"]
    data = create_comment(user_id=user_id, post_id=post_id, content=content)
    
    return ok(data=data, message="Comment created", status=201)

@bp.get("/posts/<int:post_id>/comments")
@require_auth_token
def list_comments_route(post_id: int):
    user_id = g.user["user_id"]

    data = list_comments(post_id=post_id)
    return ok(data=data, message=f"post_id:{post_id}'s comments", status=200)

@bp.delete("/comments/<int:comment_id>")
@require_auth_token
def delete_comment_route(comment_id: int):
    user_id = g.user["user_id"]
    delete_comment(user_id=user_id, comment_id=comment_id)
    return ok(data={"deleted": True}, message="Comment deleted", status=200)