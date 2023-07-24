import flask

from flask import Blueprint, url_for, request, session, redirect 

from ..controllers import client, warehouse, agreement, home

bp = Blueprint("agreement", __name__, url_prefix="/agreement")

@bp.route("/")
def index():
    return agreement.index()

@bp.route("/new", methods=("GET", "POST"))
def new():
    if request.method== "GET":
        
        return agreement.new()
    
    elif request.method ==  "POST":
        
        return agreement.create()