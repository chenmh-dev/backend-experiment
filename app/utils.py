#app/utils.py（统一返回工具）
from flask import jsonify

def ok(data=None, message="OK", status=200):
    return jsonify({
        "success": True,
        "data": data,
        "message": message
        }), status

def fail(code="ERROR", message="Error", status=400):
    return jsonify({
        "success": False,
        "error":{
            "code": code,
            "message": message
        }
    }), status