from __future__ import annotations
from typing import Any, Optional
from .exceptions import BadRequest

def get_json(request) -> dict:
    data = request.get_json(silent=True)
    # request body 为空或不是 JSON，都统一当 BAD_REQUEST
    if data is None:
        raise BadRequest(message="invalid json body")
    if not isinstance(data, dict):
        raise BadRequest(message="json body must be an object")
    return data

def required_str(data: dict, key: str, *, min_len: int = 1, max_len: int = 2000) -> str:
    val = data.get(key, None)
    if val is None:
        raise BadRequest(message=f"{key} is required")
    if not isinstance(val, str):
        raise BadRequest(message=f"{key} must be a string")
    s = val.strip()
    if len(s) < min_len:
        raise BadRequest(message=f"{key} is too short")
    if len(s) > max_len:
        raise BadRequest(message=f"{key} is too long")
    return s

def optional_str(data: dict, key: str, min_len: int = 1, max_len: int = 2000) -> Optional[str]:
    if key not in data:
        return None #request body里没有key返回None
    val = data.get(key)
    if val is None:
        return None #request body里key的值为None（前端为null）返回None
    if not isinstance(val, str):
        raise BadRequest(message=f"{key} must be a string")
    s = val.strip() #筛选：不让传空字符串，都是空格，太长，太短
    if len(s) < min_len:
        raise BadRequest(message=f"{key} is too short")
    if len(s) > max_len:
        raise BadRequest(message=f"{key} is too long")
    return s

def require_any(*values: Any, message: str = "no field to update"):
    if all(v is None for v in values):
        raise BadRequest(message=message)
    
def parse_pagination(request, *, default_page=1, default_page_size=10, max_page_size=100) -> tuple[int, int]:
    page_row = request.args.get("page", str(default_page))
    size_row = request.args.get("page_size", str(default_page_size))

    try:
        page = int(page_row)
        page_size = int(size_row)
    except ValueError:
        raise BadRequest(message="page and page_size must be integers")
    
    if page < 1:
        raise BadRequest(message="page must be >= 1")
    
    if page_size < 1 or page_size > max_page_size:
        raise BadRequest(message=f"page_size must be between 1 and {max_page_size}")
    
    return page, page_size

def parse_sorting(request, *, allowed_fields: list[str], default_field: str):
    sort = request.args.get("sort", default_field)
    order = request.args.get("order", "desc").lower()

    if sort not in allowed_fields:
        raise BadRequest(message=f"sort must be one of {allowed_fields}")
    
    if order not in ("asc", "desc"):
        raise BadRequest(message="order must be asc or desc")
    
    return sort, order

def parse_keyword(request, *, max_len=100):
    keyword = request.args.get("keyword", None)
    if keyword is None:
        return None
    
    if not isinstance(keyword, str):
        raise BadRequest(message="keyword must be a string")
    
    keyword = keyword.strip()
    if len(keyword) > max_len:
        raise BadRequest(message="keyword too long")
    
    return keyword if keyword else None