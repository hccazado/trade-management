from flask import Blueprint, request, redirect, url_for

from ..controllers import auth, buyer

bp = Blueprint("buyer", __name__, url_prefix="/buyer")

@bp.route("/")
@auth.login_required
def index():
    return buyer.index()

@bp.route("/new", methods=("GET", "POST"))
@auth.login_required
def new():
    if request.method == "GET":
        return buyer.new()
    elif request.method == "POST":
        return buyer.create()

@bp.route("/edit/<id>", methods=("GET", "POST"))
@auth.login_required
def edit(id):
    if request.method == "GET":
        return buyer.edit(id)
    elif request.method == "POST":
        return buyer.update(id)
