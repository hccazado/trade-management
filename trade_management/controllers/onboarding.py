from flask import request, session, redirect, render_template, flash, url_for, g

from ..models import user as model_user
from ..models import tenant as model_tenant


def index():
    return render_template("onboarding/index.html")


def complete():
    business_name = request.form.get("business_name", "").strip()

    if not business_name:
        flash("Informe o nome do seu negócio.")
        return render_template("onboarding/index.html")

    tenant_id = session["tenant_id"]
    model_tenant.update(tenant_id, {"name": business_name})
    model_user.complete_onboarding(session["user"])

    session.pop("onboarding", None)
    g.tenant_id = tenant_id

    return redirect(url_for("home.index"))
