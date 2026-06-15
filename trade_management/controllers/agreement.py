from datetime import datetime

from flask import url_for, request, redirect, render_template, flash

from ..models import client as model_client, warehouse as model_warehouse, agreement as model_agreement
from ..controllers import client as controller_client, warehouse as controller_warehouse


def index():
    agreements = model_agreement.get_all()
    clients = {c['id']: c['nome'] for c in model_client.get_all()}
    warehouses = {w['id']: w['nome'] for w in model_warehouse.get_all()}
    for item in agreements:
        item['comprador'] = clients.get(item.get('comprador', ''), '')
        item['vendedor'] = clients.get(item.get('vendedor', ''), '')
        item['retirada'] = warehouses.get(item.get('retirada', ''), '')
        item['descarga'] = warehouses.get(item.get('descarga', ''), '')
    ordered = sorted(agreements, key=lambda i: int(i.get('index') or 0), reverse=True)
    return render_template("app/agreement_main.html", agreements=ordered)

def new():
    clients = controller_client.sort_name(model_client.get_all())
    warehouses = controller_warehouse.sort_name(model_warehouse.get_all())
    return render_template("app/agreement_form.html", warehouses=warehouses, clients=clients)

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
        return redirect(url_for("agreement.index"))
    return render_template("app/agreement_form.html", flash("Something Went Wrong!"))

def edit(id):
    old_agreement = model_agreement.get_one(id)
    clients = controller_client.sort_name(model_client.get_all())
    warehouses = controller_warehouse.sort_name(model_warehouse.get_all())
    return render_template("app/agreement_form.html", old_agreement=old_agreement, clients=clients, warehouses=warehouses, isEditing=True)

def update(id):
    if id is None:
        return render_template("app/agreement_form.html", flash("Something Went Wrong! An ID must be informed!"))
    new_data = request.form.to_dict()
    if model_agreement.update(id, new_data):
        flash("Successfully Updated!")
        return redirect(url_for("agreement.index"))
    return render_template("app/agreement_form.html", flash("Something Went Wrong!"))

def print(id):
    agreement = model_agreement.get_one(id)
    if not agreement:
        flash("Agreement not found.")
        return redirect(url_for("agreement.index"))
    buyer = model_client.get_one(agreement["comprador"])
    seller = model_client.get_one(agreement["vendedor"])
    origin = model_warehouse.get_one(agreement["retirada"])
    delivery = model_warehouse.get_one(agreement["descarga"])
    return render_template("app/agreement.html", agreement=agreement, buyer=buyer, seller=seller, origin=origin, delivery=delivery)

def current_date():
    return datetime.now().strftime("%d/%m/%y")

def new_index():
    agreements = model_agreement.get_all()
    if not agreements:
        return 1
    return max(int(a['index']) for a in agreements) + 1

def generate_agreement_number():
    agreements = model_agreement.get_all()
    current_year = datetime.now().strftime("%y")
    current_agreements = [a for a in agreements if _is_current_year(a, current_year)]
    if not current_agreements:
        return "001/" + current_year
    ordered = sorted(current_agreements, key=lambda a: a['num_fechamento'], reverse=True)
    last_num = ordered[0]["num_fechamento"].split("/")[0]
    return str(int(last_num) + 1).zfill(3) + "/" + current_year

def _is_current_year(agreement, current_year):
    parts = agreement.get("data", "").split("/")
    return len(parts) >= 3 and parts[2] == current_year

def split_agreement(agreement):
    splited = agreement.split("/")
    return splited[0] + ", " + splited[1]
