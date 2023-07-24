import flask

from flask import Blueprint, url_for, request, session, redirect, render_template, flash

from ..db import db

from ..models import client, warehouse, agreement

clients_ref = db.get_db().collection("clients")

warehouse_ref = db.get_db().collection("warehouses")

def index():

    agreements = agreement.get_all()

    for item in agreements:

        item['comprador'] = client.get_name(item['comprador'])
        item['vendedor'] = client.get_name(item['vendedor'])
        item['descarga'] = warehouse.get_name(item['descarga'])

    return render_template("app/agreement_main.html", agreements=agreements)

def new():
    
    clients = client.get_all()

    warehouses_stream = warehouse_ref.get()

    warehouse_structure = {}
    
    warehouses = []
    
    for warehouse in warehouses_stream:
        
        warehouse_structure = warehouse.to_dict()
        
        warehouse_structure["id"] = warehouse.id
      
        warehouses.append(warehouse_structure)

    return render_template("app/agreement_form.html", warehouses=warehouses, clients = clients)

def create():
    new_agreement = request.form.to_dict()
    
    if agreement.create(new_agreement):

        return redirect(url_for("agreement.index"))
    
    else: 
        
        return render_template("app/agreement_form", flash("Something Went Wrong!"))