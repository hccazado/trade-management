import flask, json

from flask_cors import cross_origin

from flask import Blueprint, url_for, request, session, redirect, jsonify

from ..controllers import client, warehouse, agreement, auth, api

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.route("/client/<query>")
@cross_origin()
def query_client(query):

    result = api.query_clients(query)

    return json.dumps(result)

@bp.route("/warehouse/<query>")
def query_warehouse(query):

    result = api.query_warehouses(query)

    return json.dumps(result)

@bp.route("/agreement/<query>")
def query_agreements(query):

    result = api.query_agreements(query)

    return json.dumps(result)