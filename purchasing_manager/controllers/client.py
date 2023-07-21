import flask, asyncio

from flask import Blueprint, url_for, request, session, redirect, render_template

from ..db import db

clients_ref = db.get_db().collection("clients")

def index():
    
    stream = clients_ref.get()
    
    client_structure = {}
    
    clients = []
    
    for client in stream:
        
        client_structure = client.to_dict()
        
        client_structure["id"] = client.id
      
        clients.append(client_structure)
    
    return render_template("app/client_main.html", clients = clients)

def new():
    
    return render_template("app/client_form.html")

def create():
    
    document = clients_ref.document()
    
    new_client = request.form.to_dict()
    
    print(new_client)
    
    if document.set(new_client):
    
        return True
    
    else:
        
        return False

def edit(id):
    
    client = clients_ref.get(id)
    
    return render_template("app/client_form.html", isediting=True, client = client)

def update(id):
    
    new_data = request.form.to_dict()
    
    if clients_ref.document(id).set(new_data):
    
        return True
    
    else:
        
        return False