import flask

from flask import Blueprint, url_for, request, session, redirect, flash

from ..controllers import agreement, auth

bp = Blueprint("agreement", __name__, url_prefix="/agreement")

@bp.route("/")
@auth.login_required
def index():
    return agreement.index()

@bp.route("/new", methods=("GET", "POST"))
@auth.login_required
def new():
    if request.method == "GET":
        
        return agreement.new()
    
    elif request.method ==  "POST":
        
        return agreement.create()
    
@bp.route("/edit/<id>", methods=("GET", "POST"))
@auth.login_required
def edit(id):
    if request.method == "GET":
        
        return agreement.edit(id)
    
    elif request.method == "POST":
        
        return agreement.update(id)
    
@bp.route("/print/<id>")
@auth.login_required
def print(id):
    if(request.method == "GET"):

        return agreement.print(id)

    else:

        flash("Invalid Operation!")

        return redirect(url_for("home.index"))

@bp.route("/view/<id>")
@auth.login_required
def view(id):
    return flask.render_template("app/agreement_view.html",
                                 print_url=url_for("agreement.print", id=id),
                                 back_url=url_for("agreement.index"))