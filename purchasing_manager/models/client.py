from flask import current_app
from firebase_admin import exceptions
from ..db import db

#Defining Clients Firebase collection
clients_ref = db.get_db().collection("clients")

def create(new_data):
    
    try:
        
        doc = clients_ref.document()
        
        doc.set(new_data)
        
        return True
    
    except exceptions.FirebaseError as fire_error:
            
        print(fire_error.http_response, fire_error.cause)
            
        return False

def get_all():
     
    stream = clients_ref.get()
    
    client_structure = {}
    
    clients = []
    
    for client in stream:
        
        client_structure = client.to_dict()
        
        client_structure["id"] = client.id
      
        clients.append(client_structure)

    return clients

def get_one(id = None):
    
    if id == None:
        
        return {}
    
    if len(current_app.clients_collection) == 0:
        
        current_app.clients_collection = get_all()
    
    for client in current_app.clients_collection:
        
        if client['id'] == id:
            
            return client
        
def get_name(id):
    
    for client in current_app.clients_collection:
        
        if client['id'] == id:
            
            return client['nome']
        
    return ""

def update(id, new_data):
    
    try:
        
        doc = clients_ref.document(id)
        
        res = doc.set(new_data)
        
        if "update_time" in res:
            
            return True
        
        else:
            
            return False
    
    except exceptions.FirebaseError as fire_error:
            
        print(fire_error.http_response, fire_error.cause)
            
        return False

