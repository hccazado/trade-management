import flask

from flask import Blueprint, url_for, request, session, redirect, render_template, flash, current_app

from ..db import db

from ..models import warehouse as model_warehouse

def index():
    
    warehouses = current_app.warehouses_collection
            
    return render_template("app/warehouse_main.html", warehouses = warehouses)

def new():
    
    return render_template("app/warehouse_form.html")

def create():
    
    new_data = request.form.to_dict()
    
    if model_warehouse.create(new_data):
        
        current_app.warehouses_collection = model_warehouse.get_all()
    
        return True
    
    else:
        
        return False

def edit(id):
    
    warehouse = model_warehouse.get_one(id)
    
    if 'id' in warehouse:

        return render_template("app/warehouse_form.html", isediting=True, warehouse = warehouse)
    
    else:
        
        error = "Something Went Wrong. Item Not found!"
        
        flash(error)
        
        return render_template("app/warehouse_main.html")

def update(id):
    
    new_data = request.form.to_dict()
    
    if model_warehouse.update(id, new_data):
        
        current_app.warehouses_collection = model_warehouse.get_all()
    
        return redirect(url_for('home.index'))
    
    else:
        
        return render_template(url_for('app/warehouse_main.html', flash("Something went wrong!")))
        #return False