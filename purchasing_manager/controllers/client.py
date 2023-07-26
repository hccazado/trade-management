import flask, asyncio

from flask import Blueprint, url_for, request, session, redirect, render_template, flash, current_app

from ..models import client as model_client


def index():
            
    clients= current_app.clients_collection
    
    return render_template("app/client_main.html", clients = clients)

def new():
    
    return render_template("app/client_form.html", uf=current_app.uf_list)

def create():
    
    new_data = request.form.to_dict()
    
    if model_client.create(new_data):
        
        update_clients_collection()
    
        return True
    
    else:
        
        return False

def edit(id):
    
    client = model_client.get_one(id)
    
    if 'id' in client:
        
        return render_template("app/client_form.html", isediting=True, client = client, uf=current_app.uf_list)
    
    else:
        error = "Something went wrong. Register a new client?"
        flash(error)
        return render_template("app/client_form.html", isediting=False, uf=current_app.uf_list)

def update(id):
    
    new_data = request.form.to_dict()
    
    if model_client.update(id, new_data):
        
        update_clients_collection()
            
        current_app.clients_collection = model_client.get_all()

        return redirect(url_for("home.index"))
    
    else:
        
        return False
    
def update_clients_collection():
    
    current_app.clients_collection = model_client.get_all()