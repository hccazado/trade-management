import flask

from datetime import datetime

from flask import Blueprint, url_for, request, session, redirect, render_template, flash, current_app

from ..models import client as model_client, warehouse as model_warehouse, agreement as model_agreement

from ..controllers import client as controller_client, warehouse as controller_warehouse

def split_agreement(agreement):
    
    splited = agreement.split("/")
    
    return splited[0] + ", " + splited[1]

def index():

    agreements = model_agreement.get_all()

    if len(current_app.clients_collection) == 0:

        current_app.clients_collection = model_client.get_all()

        current_app.warehouses_collection = model_warehouse.get_all()


    for item in agreements:

        item['comprador'] = model_client.get_name(item['comprador'])
        
        item['vendedor'] = model_client.get_name(item['vendedor'])
        
        item['retirada'] = model_warehouse.get_name(item['retirada'])
        
        item['descarga'] = model_warehouse.get_name(item['descarga'])
        
    index_function = lambda item: int(item['index'])
        
    ordered_list = sorted(agreements, key=index_function, reverse=True)
   
    return render_template("app/agreement_main.html", agreements=ordered_list)

def new():
    
    if len(current_app.clients_collection) == 0 or len(current_app.warehouses_collection) == 0:
        
            current_app.clients_collection = controller_client.update_clients_collection()
            
            current_app.warehouses_collection = controller_warehouse.update_warehouses_collection()
        
    clients = controller_client.sort_name(current_app.clients_collection)
    
    warehouses = controller_warehouse.sort_name(current_app.warehouses_collection)

    return render_template("app/agreement_form.html", warehouses=warehouses, clients = clients)

def create():
    
    new_agreement = request.form.to_dict()
    
    new_agreement["data"] = current_date()
    
    new_agreement["created_at"] = datetime.now().strftime("%d/%m/%y - %H:%M")
    
    new_agreement["index"] = new_index()
    
    if len(new_agreement["num_fechamento"]) == 0:
        
        new_agreement["num_fechamento"] = generate_agreement_number()
        
    if len(new_agreement["pagamento"]) == 0:
        
        new_agreement["pagamento"] = controller_client.get_conta(new_agreement["vendedor"])
    
    if model_agreement.create(new_agreement):
        
        update_agreements_collection()

        return redirect(url_for("agreement.index"))
    
    else: 
        
        return render_template("app/agreement_form.html", flash("Something Went Wrong!"))
    
def edit(id):    
    
    old_agreement = model_agreement.get_one(id)
    
    current_app.clients_collection = model_client.get_all()

    current_app.warehouses_collection = model_warehouse.get_all()
    
    warehouses = controller_warehouse.sort_name(current_app.warehouses_collection)
        
    clients = controller_client.sort_name(current_app.clients_collection)
        
    return render_template("app/agreement_form.html", old_agreement = old_agreement, clients = clients, warehouses = warehouses, isEditing = True)
        

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

def agreements_current_year(agreement):
    """returns only dictionaries from current year"""
    
    current_yr = datetime.now().strftime("%y")
    
    split_dt = agreement["data"].split("/")
    
    agreement_yr = split_dt[2]
    
    if agreement_yr == current_yr:
        
        return agreement

def new_index():
    
    if len(current_app.agreements_collection) == 0:
        
        current_app.agreements_collection = model_agreement.get_all()
        
    index_function = lambda item: int(item['index'])
        
    current_app.agreements_collection = sorted(current_app.agreements_collection, key=index_function, reverse=True)    

    actual_index = current_app.agreements_collection[0]['index']
    
    new_index = int(actual_index) + 1
    
    return new_index

def generate_agreement_number():
    
    num_fechamento_function = lambda item: item['num_fechamento']
    
    if len(current_app.agreements_collection) == 0:
        
        current_app.agreements_collection = model_agreement.get_all()
        
    current_year = datetime.now().strftime("%y")

    current_agreements = list(filter(agreements_current_year ,current_app.agreements_collection))

    if len(current_agreements) > 0:
        
        ordered_agreements = sorted(current_agreements, key=num_fechamento_function, reverse=True)
    
        actual_agreement_number = ordered_agreements[0]["num_fechamento"]
        
        actual_agreement_number = actual_agreement_number.split("/")[0]
        
        nxt_agreement = int(actual_agreement_number) + 1 
        
        nxt_agreement = str(nxt_agreement).zfill(3)
        
        nxt_agreement += "/" + current_year
        
        return nxt_agreement
        
    else:
        
        nxt_agreement = str(1).zfill(3)
        
        nxt_agreement += "/" + current_year
        
        return nxt_agreement
    
def print(id):

    current_app.agreements_collection = model_agreement.get_all()

    current_app.clients_collection = model_client.get_all()
    
    current_app.warehouses_collection = model_warehouse.get_all()
    
    for item in current_app.agreements_collection:
        
        if item['id'] == id:
            
            buyer = model_client.get_one(item["comprador"])

            seller = model_client.get_one(item["vendedor"])

            origin = model_warehouse.get_one(item["retirada"])
            
            delivery = model_warehouse.get_one(item["descarga"])
            
            return render_template("app/agreement.html", agreement = item, buyer = buyer, seller = seller, origin = origin, delivery = delivery)
    
