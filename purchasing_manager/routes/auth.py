import flask, os

from flask import Blueprint, url_for, request, session, redirect, render_template

from ..controllers import auth as auth_controller

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=("GET", "POST"))
def login():
    
    if request.method == "GET":
        
        return render_template("auth/login.html")
    
    elif request.method == "POST":
                
        return auth_controller.login()
    
@bp.route("/new", methods=("GET", "POST"))
def new():
    
    if request.method == "GET":
        
        return render_template("auth/new.html")
    
    elif request.method == "POST":
        
        return auth_controller.create()
    
@bp.route("/logout")
def logout():
    
    return auth_controller.logout()