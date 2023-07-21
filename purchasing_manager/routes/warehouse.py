import flask

from flask import Blueprint, url_for, request, session, redirect 

from ..controllers import warehouse

bp = Blueprint("warehouse", __name__, url_prefix="/warehouse")

@bp.route("/")
def index():
    return warehouse.index()

@bp.route("/new", methods=("GET", "POST"))
def new():
    if request.method == "GET":
       
        return warehouse.new()
    
    elif request.method == "POST":
        
        if warehouse.create():
            
            return redirect(url_for("warehouse.index"))
        
@bp.route("/edit/<id>", methods = ("GET", "POST"))
def update(id):
    
    if request.method == "GET":
        
        return warehouse.edit(id)
    
    elif request.method == "POST":
        
        return warehouse.update(id)