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
    
    if document.set(new_warehouse):
    
        return True
    
    else:
        
        return False

def edit(id):
    
    stream =  warehouses_ref.document(id).get()
    
    warehouse_structure = {} 
    
    warehouse_structure = stream.to_dict()
        
    warehouse_structure["id"] = stream.id 
    
    if warehouse_structure:

        return render_template("app/warehouse_form.html", isediting=True, warehouse = warehouse_structure)
    
    else:
        
        error = "Something Went Wrong. Item Not found!"
        
        flash(error)
        
        return render_template("app/warehouse_main.html")

def update(id):
    
    new_data = request.form.to_dict()
    
    res = warehouses_ref.document(id).set(new_data)

    if "update_time" in res:
    
        return redirect(url_for('home.index'))
    
    else:
        
        return render_template(url_for('app/warehouse_main.html', flash("Something went wrong!")))
        #return False