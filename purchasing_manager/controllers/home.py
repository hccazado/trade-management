import flask

from flask import Blueprint, url_for, request, session, redirect, render_template

def index():
    """Render index view"""
    return render_template("app/index.html")