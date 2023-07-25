import flask, asyncio

from flask import Blueprint, url_for, request, session, redirect, render_template, flash, g

from ..db import db

from ..models import client as model_client

clients_ref = db.get_db().collection("clients")

def index():
    
   #stream = clients_ref.get()
    
    #client_structure = {}
    
    #clients = []
    
    #for client in stream:
        
        #client_structure = client.to_dict()
        
        #client_structure["id"] = client.id
      
        #clients.append(client_structure)
        
    clients= g.clients_collection.copy()
    
    return render_template("app/client_main.html", clients = clients)

def new():
    
    return render_template("app/client_form.html")

def create():
    
    document = clients_ref.document()
    
    new_client = request.form.to_dict()
    
    if document.set(new_client):
        
        g.clients_collection = model_client.get_all()
    
        return True
    
    else:
        
        return False

def edit(id):
    
    client = clients_ref.document(id).get()
    
    client_structure = client.to_dict()
        
    client_structure["id"] = client.id
    
    if client_structure:
        
        g.clients_collection = model_client.get_all()
    
        return render_template("app/client_form.html", isediting=True, client = client_structure)
    
    else:
        error = "Something went wrong. Register a new client?"
        flash(error)
        return render_template("app/client_form.html", isediting=False)

def update(id):
    
    new_data = request.form.to_dict()

    res = clients_ref.document(id).set(new_data)

    
    if "update_time" in res:

        return redirect(url_for("home.index"))
    
    else:
        
        return False