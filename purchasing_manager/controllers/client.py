from flask import url_for, request, redirect, render_template, flash, current_app

from ..models import client as model_client


def index():
    clients = sort_name(model_client.get_all())
    return render_template("app/client_main.html", clients=clients)

def new():
    return render_template("app/client_form.html", uf=current_app.uf_list)

def create():
    new_data = request.form.to_dict()
    if model_client.create(new_data):
        return True
    return False

def edit(id):
    client = model_client.get_one(id)
    if 'id' in client:
        return render_template("app/client_form.html", isediting=True, client=client, uf=current_app.uf_list)
    flash("Something went wrong. Register a new client?")
    return render_template("app/client_form.html", isediting=False, uf=current_app.uf_list)

def update(id):
    new_data = request.form.to_dict()
    if model_client.update(id, new_data):
        return redirect(url_for("home.index"))
    return False

def get_conta(id):
    client = model_client.get_one(id)
    return client.get("conta", "")

def sort_name(clients):
    return sorted(clients, key=lambda c: c["nome"])
