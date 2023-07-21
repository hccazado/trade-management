import flask

from flask import Blueprint, url_for, request, session, redirect, render_template, flash

from ..db import db

warehouses_ref = db.get_db().collection("warehouses")

def index():
    
    stream = warehouses_ref.get()
    
    warehouse_structure = {}
    
    warehouses = []
    
    for warehouse in stream:
        
        warehouse_structure = warehouse.to_dict()
        
        warehouse_structure["id"] = warehouse.id
      
        warehouses.append(warehouse_structure)
    
    return render_template("app/warehouse_main.html", warehouses = warehouses)

def new():
    
    return render_template("app/warehouse_form.html")

def create():
    
    document = warehouses_ref.document()
    
    new_warehouse = request.form.to_dict()
    
    print(new_warehouse)
    
    if document.set(new_warehouse):
    
        return True
    
    else:
        
        return False

def edit(id):
    
    warehouse = warehouses_ref.get(id)
    
    if id in warehouse:

        return render_template("app/warehouse_form.html", isediting=True, warehouse = warehouse)
    
    else:
        
        error = "Not found!"
        
        flash(error)
        
        return render_template("app/warehouse_main.html")

def update(id):
    
    new_data = request.form.to_dict()
    
    if warehouses_ref.document(id).set(new_data):
    
        return True
    
    else:
        
        return False