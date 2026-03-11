from flask import Blueprint
from .utils import ok,fail

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return ok(message="Home Page")