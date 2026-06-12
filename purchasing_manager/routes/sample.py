from flask import Blueprint, url_for, request, session, redirect 

from ..controllers import sample, auth

bp = Blueprint("sample", __name__, url_prefix="/sample")

@bp.route("/")
@auth.login_required
def index():
    return sample.index()

@bp.route("/new", methods = ("GET", "POST"))
@auth.login_required
def new():
    if request.method == "GET":
        return sample.new()
    elif request.method == "POST":
        return sample.create()

@bp.route("/edit/<id>", methods = ("GET", "POST"))
@auth.login_required
def edit(id):
    if request.method == "GET":
        return sample.edit(id)
    elif request.method == "POST":
        return sample.update(id)

@bp.route("/notify/<id>", methods=("POST",))
@auth.login_required
def notify(id):
    return sample.notify(id)
