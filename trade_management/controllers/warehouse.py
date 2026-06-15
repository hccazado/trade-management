from flask import url_for, request, redirect, render_template, flash, current_app

from ..models import warehouse as model_warehouse


def index():
    warehouses = sort_name(model_warehouse.get_all())
    return render_template("app/warehouse_main.html", warehouses=warehouses, uf=current_app.uf_list)

def new():
    return render_template("app/warehouse_form.html", uf=current_app.uf_list)

def create():
    new_data = request.form.to_dict()
    if model_warehouse.create(new_data):
        return True
    return False

def create_from_dict(new_data):
    if model_warehouse.create(new_data):
        return True
    return False

def edit(id):
    warehouse = model_warehouse.get_one(id)
    if 'id' in warehouse:
        return render_template("app/warehouse_form.html", isediting=True, warehouse=warehouse, uf=current_app.uf_list)
    flash("Something Went Wrong. Item Not found!")
    return render_template("app/warehouse_main.html")

def update(id):
    new_data = request.form.to_dict()
    if model_warehouse.update(id, new_data):
        return redirect(url_for('home.index'))
    return render_template(url_for('app/warehouse_main.html', flash("Something went wrong!")))

def sort_name(warehouses):
    return sorted(warehouses, key=lambda w: w["nome"])
