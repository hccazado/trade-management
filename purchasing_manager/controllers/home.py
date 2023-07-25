import flask

from flask import Blueprint, url_for, request, session, redirect, render_template

def index():
    return render_template("app/index.html")