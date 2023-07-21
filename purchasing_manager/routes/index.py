import flask

from flask import Blueprint, url_for, request, session, redirect 

from ..controllers import index


#declaring routing for index controller
bp = Blueprint("index", __name__, url_prefix="/")

@bp.route("/")
def home():
    return index.index()