users = {
    "hui": "123",
    "alice": "456"
}

from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__) 
app.config["JSON_SORT_KEYS"] = False
"""Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass"""
'''.\venv\Scripts\activate'''
@app.route("/")
def home():
    return "this is 晖" #http://127.0.0.1:5000/

@app.route("/contact")
def contact():
    return "this is contact"

@app.route("/profile")
def profile():
    return {
        "name": "晖",
        "skill": "Flask Beginner",
        "day": 2
    }

@app.route("/skill")
def skill():
    return{["Python","Flask","Debugging"]}

@app.route("/user/<name>")
def user(name):
    return {
        "user": f"{name}",
        "message": f"Hello {name}",
        "status": "active"
    }

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    limit = request.args.get("limit", type=int)
    if not keyword:
        return {"error": "keyword is required"}
    else:
        return {
            "keyword": keyword,
            "limit": limit,
            "massage": f"you search for {keyword}"
        }
    
@app.route("/login", methods=["POST"])
def login():
    data = request.json 
    '''获取post请求体里的json数据,
    赋值给data此时flask会自动把json转换（loads）成dict类型'''

    username = data.get("username")
    password = data.get("password")
    
    if username not in users:
        return{"status": "error", "reason": "user not found"}
    
    if users[username] != password:
        return{"status": "error", "reason": "wrong password"}
    
    return {"status": "success", "message": "login success"}

if __name__ == "__main__":
    app.run(debug=True)