import flask

from flask import Blueprint, url_for, request, session, redirect 

from ..controllers import client, warehouse, agreement, index

bp = Blueprint("agreement", __name__, url_prefix="/warehouse")