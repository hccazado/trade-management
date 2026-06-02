import json

from flask_cors import cross_origin
from flask import Blueprint

from ..controllers import auth, api

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.route("/client/<query>")
@cross_origin()
@auth.login_required
def query_client(query):
    return json.dumps(api.query_clients(query))

@bp.route("/warehouse/<query>")
@auth.login_required
def query_warehouse(query):
    return json.dumps(api.query_warehouses(query))

@bp.route("/agreement/<query>")
@auth.login_required
def query_agreements(query):
    return json.dumps(api.query_agreements(query))

@bp.route("/sample/<query>")
@auth.login_required
def query_samples(query):
    return json.dumps(api.query_samples(query))
