from datetime import datetime

from flask import url_for, request, redirect, render_template, flash

from ..models import client as model_client, sample as model_sample
from ..controllers import client as controller_client


def index():
    samples = model_sample.get_all()
    for item in samples:
        client_id = item.get('client', '')
        item['client_name'] = model_client.get_name(client_id) if client_id else "Sem Cliente"
    samples = sorted(samples, key=lambda s: s.get('num_amostra', ''), reverse=True)
    return render_template("app/sample_main.html", samples=samples)

def new():
    clients = controller_client.sort_name(model_client.get_all())
    today_str = datetime.now().strftime("%d/%m/%y")
    return render_template("app/sample_form.html", clients=clients, today=today_str)

def create():
    new_data = request.form.to_dict()
    if 'client' not in new_data:
        new_data['client'] = ""
    if not new_data.get("num_amostra"):
        new_data["num_amostra"] = generate_sample_number()
    if model_sample.create(new_data):
        flash("Amostra cadastrada com sucesso!")
        return redirect(url_for("sample.index"))
    flash("Ocorreu um erro ao cadastrar a amostra.", "error")
    return redirect(url_for("sample.new"))

def edit(id):
    sample = model_sample.get_one(id)
    clients = controller_client.sort_name(model_client.get_all())
    if 'id' in sample:
        return render_template("app/sample_form.html", isediting=True, sample=sample, clients=clients)
    flash("Amostra não encontrada.", "error")
    return redirect(url_for("sample.index"))

def update(id):
    new_data = request.form.to_dict()
    if 'client' not in new_data:
        new_data['client'] = ""
    if model_sample.update(id, new_data):
        flash("Amostra atualizada com sucesso!")
        return redirect(url_for("sample.index"))
    flash("Ocorreu um erro ao atualizar a amostra.", "error")
    return redirect(url_for("sample.edit", id=id))

def generate_sample_number():
    samples = model_sample.get_all()
    current_year = datetime.now().strftime("%y")
    valid = [s for s in samples if _is_current_year(s, current_year) and "/" in s.get("num_amostra", "")]
    if not valid:
        return "001/" + current_year
    ordered = sorted(valid, key=lambda s: s.get("num_amostra", ""), reverse=True)
    last_seq = ordered[0]["num_amostra"].split("/")[0]
    try:
        nxt = int(last_seq) + 1
    except ValueError:
        nxt = len(valid) + 1
    return str(nxt).zfill(3) + "/" + current_year

def _is_current_year(sample, current_year):
    parts = sample.get("data", "").split("/")
    return len(parts) >= 3 and parts[2] == current_year
