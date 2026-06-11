from flask import request, redirect, render_template, url_for, flash

from ..models import buyer as model_buyer

TIPO_OPTIONS = ['fine', 'verygood', 'good', 'bica', 'barrento', 'escolha', 'chuvado', 'fd10']
BEBIDA_OPTIONS = ['Duro', 'Riado', 'Rio', 'Fermentado', 'Sujo']
PENEIRA_OPTIONS = [
    {'field': 'pen_17_8', 'label': '17/8',  'sample_key': '17/8'},
    {'field': 'pen_13',   'label': '13',     'sample_key': '13'},
    {'field': 'pen_10',   'label': '10',     'sample_key': '10'},
    {'field': 'pen_mk',   'label': 'Moka',   'sample_key': 'Mk'},
    {'field': 'pen_fd',   'label': 'Fundo',  'sample_key': 'FD'},
    {'field': 'pen_cata', 'label': 'Catado', 'sample_key': 'Cata'},
    {'field': 'pen_pva',  'label': 'Defeitos','sample_key': 'PVA'},
    {'field': 'pen_broca','label': 'Broca',  'sample_key': 'Broca'},
]

def _to_float(value, default=None):
    if value is None or value == '':
        return default
    try:
        return float(str(value).replace('%', '').strip())
    except (ValueError, TypeError):
        return default


def _peneiras_match(sample, buyer):
    tolerancia = _to_float(buyer.get('peneiras_tolerancia'), default=0.0)
    for p in PENEIRA_OPTIONS:
        min_val = _to_float(buyer.get(p['field']))
        if min_val is None:
            continue
        sample_val = _to_float(sample.get(p['sample_key']))
        if sample_val is None:
            return False
        if sample_val < (min_val - tolerancia):
            return False
    return True


def _bebida_match(sample, buyer):
    preferred = set(buyer.get('bebida') or [])
    if not preferred:
        return True
    tolerancia = int(_to_float(buyer.get('bebida_tolerancia'), default=0))
    has_preferred = any(int(sample.get(b) or 0) > 0 for b in preferred)
    if not has_preferred:
        return False
    non_preferred = set(BEBIDA_OPTIONS) - preferred
    other_cups = sum(int(sample.get(b) or 0) for b in non_preferred)
    return other_cups <= tolerancia


def get_matching_buyers(sample):
    buyers = model_buyer.get_all()
    result = []
    for buyer in buyers:
        if not buyer.get('ativo'):
            continue
        tipo_list = buyer.get('tipo') or []
        if tipo_list and sample.get('tipo') not in tipo_list:
            continue
        qty_min = _to_float(buyer.get('quantidade_minima'))
        if qty_min is not None:
            if _to_float(sample.get('quantidade'), default=0.0) < qty_min:
                continue
        if not _peneiras_match(sample, buyer):
            continue
        if not _bebida_match(sample, buyer):
            continue
        result.append(buyer)
    return result


def _template_ctx():
    return dict(tipo_options=TIPO_OPTIONS, bebida_options=BEBIDA_OPTIONS, peneira_options=PENEIRA_OPTIONS)


def index():
    buyers = sorted(model_buyer.get_all(), key=lambda b: b.get("nome", ""))
    return render_template("app/buyer_main.html", buyers=buyers)

def new():
    return render_template("app/buyer_form.html", **_template_ctx())

def create():
    new_data = request.form.to_dict()
    if not new_data.get("nome") or not new_data.get("whatsapp"):
        flash("Nome e WhatsApp são obrigatórios.")
        return render_template("app/buyer_form.html", **_template_ctx())
    whatsapp = new_data.get("whatsapp", "")
    if not whatsapp.startswith("+55"):
        new_data["whatsapp"] = "+55" + whatsapp
    new_data["tipo"] = request.form.getlist("tipo")
    new_data["bebida"] = request.form.getlist("bebida")
    new_data["ativo"] = new_data.get("ativo") == "on"
    if model_buyer.create(new_data):
        return redirect(url_for("buyer.index"))
    flash("Erro ao cadastrar comprador.")
    return render_template("app/buyer_form.html", **_template_ctx())

def edit(id):
    buyer = model_buyer.get_one(id)
    if "id" in buyer:
        return render_template("app/buyer_form.html", isediting=True, buyer=buyer, **_template_ctx())
    flash("Comprador não encontrado.")
    return redirect(url_for("buyer.index"))

def update(id):
    new_data = request.form.to_dict()
    if not new_data.get("nome") or not new_data.get("whatsapp"):
        flash("Nome e WhatsApp são obrigatórios.")
        buyer = model_buyer.get_one(id)
        return render_template("app/buyer_form.html", isediting=True, buyer=buyer, **_template_ctx())
    whatsapp = new_data.get("whatsapp", "")
    if not whatsapp.startswith("+55"):
        new_data["whatsapp"] = "+55" + whatsapp
    new_data["tipo"] = request.form.getlist("tipo")
    new_data["bebida"] = request.form.getlist("bebida")
    new_data["ativo"] = new_data.get("ativo") == "on"
    if model_buyer.update(id, new_data):
        return redirect(url_for("buyer.index"))
    flash("Erro ao atualizar comprador.")
    buyer = model_buyer.get_one(id)
    return render_template("app/buyer_form.html", isediting=True, buyer=buyer, **_template_ctx())
