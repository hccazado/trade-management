import glob
import os
import secrets

from flask import current_app, request, render_template, redirect, url_for, flash, session

from ..models import admin as model_admin
from ..models import tenant as model_tenant
from ..models import user as model_user

MAX_LOGO_BYTES = 200 * 1024  # 200 KB


def index():
    tenants = model_admin.get_all_tenants()
    return render_template("admin/index.html", tenants=tenants)


def tenant_detail(id):
    tenants = model_admin.get_all_tenants()
    tenant = next((t for t in tenants if t["id"] == id), None)
    if not tenant:
        flash("Tenant não encontrado.")
        return redirect(url_for("admin.index"))
    users = model_admin.get_tenant_users(id)
    return render_template("admin/tenant.html", tenant=tenant, users=users)


def update_tenant(id):
    name = request.form.get("name", "").strip()
    data = {}

    if name:
        data["name"] = name

    logo_file = request.files.get("logo")
    if logo_file and logo_file.filename:
        raw = logo_file.read()
        if len(raw) > MAX_LOGO_BYTES:
            flash("Logo muito grande. Máximo 200 KB.")
            return redirect(url_for("admin.tenant_detail", id=id))
        ext = logo_file.filename.rsplit(".", 1)[-1].lower() if "." in logo_file.filename else "png"
        profile_dir = os.path.join(current_app.static_folder, "profile")
        os.makedirs(profile_dir, exist_ok=True)
        for old in glob.glob(os.path.join(profile_dir, f"{id}.*")):
            os.remove(old)
        filename = f"{id}.{ext}"
        with open(os.path.join(profile_dir, filename), "wb") as f:
            f.write(raw)
        data["logo"] = f"profile/{filename}"

    if data:
        model_tenant.update(id, data)
        if session.get("tenant_id") == id and "logo" in data:
            session["tenant_logo"] = data["logo"]
        flash("Atualizado com sucesso.")
    return redirect(url_for("admin.tenant_detail", id=id))


def reset_password(user_id, tenant_id):
    temp_password = secrets.token_urlsafe(8)
    model_user.reset_password(user_id, temp_password)
    flash(f"Senha temporária: {temp_password}")
    return redirect(url_for("admin.tenant_detail", id=tenant_id))
