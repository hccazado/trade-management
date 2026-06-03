from flask import Blueprint

from ..controllers import auth, admin

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/")
@auth.admin_required
def index():
    return admin.index()


@bp.route("/tenant/<id>")
@auth.admin_required
def tenant_detail(id):
    return admin.tenant_detail(id)


@bp.route("/tenant/<id>/update", methods=["POST"])
@auth.admin_required
def update_tenant(id):
    return admin.update_tenant(id)


@bp.route("/tenant/<tenant_id>/reset/<user_id>", methods=["POST"])
@auth.admin_required
def reset_password(tenant_id, user_id):
    return admin.reset_password(user_id, tenant_id)
