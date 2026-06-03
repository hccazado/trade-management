import functools

from flask import url_for, request, session, redirect, render_template, flash, g

from werkzeug.security import check_password_hash, generate_password_hash

from .. import oauth
from ..models import user as model_user
from ..models import tenant as model_tenant


def login():

    uname = request.form["name"]
    upassword = request.form["password"]

    if not uname:
        flash("Must inform a user!")
        return render_template("auth/login.html")

    if not upassword:
        flash("Must inform a password!")
        return render_template("auth/login.html")

    session.pop("user", None)

    users = model_user.get()

    for user in users:
        if user["name"] == uname:
            if check_password_hash(user["password"], upassword):
                session["user"] = user["id"]
                session["tenant_id"] = user.get("tenant_id")
                session["is_admin"] = user.get("is_admin", False)
                g.tenant_id = session["tenant_id"]
                return redirect(url_for("home.index"))

    flash("Invalid User/Password")
    return render_template("auth/login.html")


def create():

    new_user = request.form.to_dict()
    new_user["password"] = generate_password_hash(new_user["password"])
    new_user["tenant_id"] = model_tenant.create(new_user.get("name", ""))

    if model_user.create(new_user):
        flash("User Successfully Created!")
        return redirect(url_for("auth.login"))
    else:
        flash("Something Went Wrong!")
        return redirect(url_for("auth.login"))


def logout():
    session.pop("user", None)
    return redirect(url_for("home.index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "user" not in session:
            return redirect(url_for("auth.login"))
        if session.get("onboarding"):
            return redirect(url_for("onboarding.index"))
        g.tenant_id = session["tenant_id"]
        return view(**kwargs)
    return wrapped_view


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "user" not in session:
            return redirect(url_for("auth.login"))
        if not session.get("is_admin"):
            flash("Acesso restrito.")
            return redirect(url_for("home.index"))
        return view(**kwargs)
    return wrapped_view


def google_login():
    import os
    redirect_uri = os.environ.get(
        "GOOGLE_REDIRECT_URI",
        url_for("auth.google_callback", _external=True)
    )
    print(f"OAuth redirect_uri: {redirect_uri}")
    return oauth.google.authorize_redirect(redirect_uri)


def google_callback():
    token = oauth.google.authorize_access_token()
    google_info = token.get("userinfo")
    if not google_info:
        flash("Google login failed. Please try again.")
        return redirect(url_for("auth.login"))

    user = model_user.get_or_create_google_user(google_info)
    session["user"] = user["id"]
    session["tenant_id"] = user.get("tenant_id")
    session["is_admin"] = user.get("is_admin", False)
    if user.get("onboarding"):
        session["onboarding"] = True
        return redirect(url_for("onboarding.index"))
    g.tenant_id = session["tenant_id"]
    return redirect(url_for("home.index"))
