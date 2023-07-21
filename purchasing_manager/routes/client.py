import flask

from flask import Blueprint, url_for, request, session, redirect 

from ..controllers import client, warehouse, agreement, home

bp = Blueprint("client", __name__, url_prefix="/client")

@bp.route("/")
def index():
    return client.index()

@bp.route("/new", methods = ("GET", "POST"))
def new():
    
    if request.method == "GET":
        
        return client.new()
        
    elif request.method == "POST":
        
        if client.create():
            
            return redirect(url_for("client.index"))
        
@bp.route("/edit/<id>", methods = ("GET", "POST"))
def edit(id):

    if request.method == "GET":
        
        return client.edit(id)
    
    elif request.method == "POST":
        
        return client.update(id)