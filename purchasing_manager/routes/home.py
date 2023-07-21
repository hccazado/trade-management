import flask

from flask import Blueprint, url_for, request, session, redirect 

from ..controllers import client, warehouse, agreement, home


#declaring routing for index controller
bp = Blueprint("home", __name__, url_prefix="/")

@bp.route("/")
def index():
    return home.index()