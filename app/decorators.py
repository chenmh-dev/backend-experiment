from functools import wraps
from flask import request, g
from .utils import fail
from .auth import verify_auth_token

def require_auth_token(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        auth = auth.strip()
        
        if not auth.startswith("Bearer "):
            return fail(code="UNAUTHORIZED", message="Missing Bearer token", status=401)
        
        token = auth.removeprefix("Bearer ").strip()
        data = verify_auth_token(token)
        if not data or "user_id" not in data:
            return fail(code="UNAUTHORIZED", message="Invalid or expired token", status=401)
        
        # 把登录用户信息放到 g（Flask 的请求级全局变量）
        g.user = data
        return fn(*args, **kwargs)
    
    return wrapper