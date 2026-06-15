from flask import Blueprint, request

from ..controllers import onboarding, auth

bp = Blueprint("onboarding", __name__, url_prefix="/onboarding")

@bp.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        return onboarding.complete()
    return onboarding.index()
