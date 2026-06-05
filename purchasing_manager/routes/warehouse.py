import flask

from flask import Blueprint, url_for, request, session, redirect 

from ..controllers import warehouse, auth

bp = Blueprint("warehouse", __name__, url_prefix="/warehouse")

@bp.route("/")
@auth.login_required
def index():
    
    return warehouse.index()

@bp.route("/new", methods=("GET", "POST"))
@auth.login_required
def new():
    if request.method == "GET":
       
        return warehouse.new()
    
    elif request.method == "POST":
        
        if warehouse.create():
            
            return redirect(url_for("warehouse.index"))
        
@bp.route("/edit/<id>", methods = ("GET", "POST"))
@auth.login_required
def edit(id):
    
    if request.method == "GET":
        
        return warehouse.edit(id)
    
    elif request.method == "POST":
        
        return warehouse.update(id)