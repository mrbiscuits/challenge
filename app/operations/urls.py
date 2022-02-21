from flask import current_app, jsonify
from app.operations import operations, views
from flask import render_template, redirect, session, current_app, jsonify, request, json, flash
from manage import PROJECT_ROOT
import os 

@operations.route("/api/healthcheck", methods=["GET"])
def healthcheck():
    return views.healthcheck(request)

@operations.route("/", methods=["GET"])
def home():
    return views.home(request)

@operations.route("/test", methods=["GET"])
def tests(): # pragma: no cover
    return views.runtests(request)

@operations.route("/readme", methods=["GET"])
def readme(): # pragma: no cover
    return views.readme(request)

from flask import send_from_directory

@operations.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(PROJECT_ROOT, 'app/static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')