import flask, os, requests, json, functools

from flask import Blueprint, url_for, request, session, redirect, render_template, flash, g

from werkzeug.security import check_password_hash, generate_password_hash

from ..models import user as model_user
from ..models import client as model_client
from ..models import warehouse as model_warehouse
from ..models import agreement as model_agreement

global CLIENTS

def login():

    uname = request.form["name"]
    
    upassword = request.form["password"]
    
    if not uname:
        
        error = "Must inform a user!"
        
        flash(error)
        
        return render_template("auth/login.html")
    
    elif not upassword:
        
        error = "Must inform a password!"
        
        flash(error)
        
        return render_template("auth/login.html")
    
    else:
        
        session.pop("user", None)
        
        users = model_user.get()
        
        for user in users:
            
            if user["name"] == uname:
                                
                if check_password_hash(user["password"], upassword):
                    
                    session["user"] = user["id"]
                    
                    load_snapshots()
                    
                    return redirect(url_for("home.index"))
        
        flash("Invalid User/Password")
        
        return render_template("auth/login.html")
                

def create():
    
    new_user = request.form.to_dict()
    
    new_user["password"] = generate_password_hash(new_user["password"])
    
    if model_user.create(new_user):
        
        flash("User Successfully Created!")
        
        return redirect(url_for("auth.login"))
    
    else:
        
        flash("Something Went Wrong!")
        
        return redirect(url_for("auth.login"))
    
def logout():
    session.pop("user", None)
    
    return redirect(url_for("home.index"))

def login_required(view):
    @functools.wraps(view)
    
    def wrapped_view(**kwargs):
        
        if not "user" in session:
            
            return redirect(url_for("auth.login"))
        
        return view(**kwargs)
    
    return wrapped_view
        
        
def load_snapshots():
    
    g.clients_collection = model_client.get_all()
    
    g.warehouse_collection = model_warehouse.get_all()
    