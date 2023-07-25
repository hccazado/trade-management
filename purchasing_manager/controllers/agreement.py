import flask

from datetime import datetime

from flask import Blueprint, url_for, request, session, redirect, render_template, flash, current_app

from ..db import db

from ..models import client as model_client, warehouse as model_warehouse, agreement as model_agreement

def index():

    agreements = model_agreement.get_all()

    for item in agreements:

        item['comprador'] = model_client.get_name(item['comprador'])
        item['vendedor'] = model_client.get_name(item['vendedor'])
        item['retirada'] = model_warehouse.get_name(item['retirada'])
        item['descarga'] = model_warehouse.get_name(item['descarga'])

    print(current_app.agreements_collection)
    
    generate_agreement_number()
    
    return render_template("app/agreement_main.html", agreements=agreements)

def new():
    
    clients = current_app.clients_collection
    
    warehouses = current_app.warehouses_collection

    return render_template("app/agreement_form.html", warehouses=warehouses, clients = clients)

def create():
    
    new_agreement = request.form.to_dict()
    
    new_agreement["data"] = current_date()
    
    new_agreement["created_at"] = datetime.now().strftime("%d/%m/%y - %H:%M")
    
    if model_agreement.create(new_agreement):
        
        update_agreements_collection()

        return redirect(url_for("agreement.index"))
    
    else: 
        
        return render_template("app/agreement_form.html", flash("Something Went Wrong!"))
    
def edit(id):
    
    if (id == None):
        
        return render_template("app/agreement_form.html", flash("Something Went Wrong! An ID must be informed!"))
    
    old_agreement = model_agreement.get_one(id)
    
    if 'id' in old_agreement:
        
        clients = current_app.clients_collection
    
        warehouses = current_app.warehouses_collection
        
        for client in clients:
            
            if client['id'] == old_agreement['vendedor']:
                print("vendedor - match")
                
            if client['id'] == old_agreement['comprador']:
                print("comprador - match")
        
        return render_template("app/agreement_form.html", old_agreement = old_agreement, clients = clients, warehouses = warehouses, isEditing = True)
    
    else:
        
        flash("Something Went Wrong! Informed ID Not Found!")
        
        return render_template("app/agreement_main.html")

def update (id):
    
    if (id == None):
        
        return render_template("app/agreement_form.html", flash("Something Went Wrong! An ID must be informed!"))
    
    else:
    
        new_data = request.form.to_dict()
        
        if model_agreement.update(id, new_data):
            
            update_agreements_collection()
            
            flash("Successfully Updated!")
        
            return redirect(url_for("agreement.index"))
        
        else:
            
           return render_template("app/agreement_form.html", flash("Something Went Wrong!")) 
       
def update_agreements_collection():
    current_app.agreements_collection = model_agreement.get_all()
    
def current_date():
    
    current_dt = datetime.now().strftime("%d/%m/%y")
    
    return current_dt

def generate_agreement_number():
    
    created_at_function = lambda item: item['created_at']
    
    if len(current_app.agreements_collection) > 0:
    
        ordered_list = sorted(current_app.agreements_collection, key=created_at_function)
            
        identifier_struct = ordered_list[-1]['num_fechamento'].split("/")
        
        print(identifier_struct[0])
    
    #print (identifier_struct)
    
    #actual_agreement_count = identifier_struct[0]
    
    #if not actual_agreement_count:
        
    #    actual_agreement_count = "Not found"
    
    #print(actual_agreement_count)
        
def print(id):
    
    for item in current_app.agreements_collection:
        
        if item['id'] == id:
            
            buyer = model_client.get_one(item["comprador"])
            seller = model_client.get_one(item["vendedor"])
            origin = model_client.get_one(item["retirada"])
            delivery = model_client.get_one(item["descarga"])
            
            return render_template("app/agreement.html", agreement = item, buyer = buyer, seller = seller, origin = origin, delivery = delivery)
    