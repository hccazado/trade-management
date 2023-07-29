from flask import current_app

from ..db import db

from firebase_admin import exceptions

warehouses_ref = db.get_db().collection("warehouses")

def get_all():
    stream = warehouses_ref.get()
    
    warehouse_structure = {}
    
    warehouses = []
    
    for warehouse in stream:
        
        warehouse_structure = warehouse.to_dict()
        
        warehouse_structure["id"] = warehouse.id
      
        warehouses.append(warehouse_structure)
        
    return warehouses

def get_one(id = None):
    
    if id == None:
        
        return {}
    
    if len(current_app.warehouses_collection) == 0:
        
        current_app.warehouses_collection = get_all()
    
    for warehouse in current_app.warehouses_collection:
        
        if warehouse['id'] == id:
    
            return warehouse    

def get_name(id):
    
    for warehouse in current_app.warehouses_collection:
        
        if warehouse['id'] == id:
            
            return warehouse['nome']

def create(new_data):
    
    try:
        
        doc = warehouses_ref.document()
        
        doc.set(new_data)

        return True
            
    except exceptions.FirebaseError as fire_error:
            
        print(fire_error.http_response, fire_error.cause)
            
        return False

def update(id, new_data):
    
    try:
        
        document = warehouses_ref.document(id)
    
        res = document.set(new_data)
    
        if "update_time" in res:
        
            return True
    
        else:
        
            return False
            
    except exceptions.FirebaseError as fire_error:
            
        print(fire_error.http_response, fire_error.cause)
            
        return False