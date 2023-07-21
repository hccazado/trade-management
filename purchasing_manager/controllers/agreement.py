import flask

from flask import Blueprint, url_for, request, session, redirect, render_template

from ..db import db

def index():
    return render_template("app/agreement_main.html")
