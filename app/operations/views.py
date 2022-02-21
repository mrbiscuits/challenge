import time
from flask import render_template, redirect, session, current_app, jsonify, request, json, flash
from flask import current_app, flash
from datetime import datetime, timedelta
from flask import abort, jsonify
import subprocess 
from manage import PROJECT_ROOT

def home(request):
    return render_template("index.html", app_name="challenges")

def healthcheck(request):
    return jsonify({'status': 'OK'})

def runtests(request): # pragma: no cover
    print(f'pytest --cov="{PROJECT_ROOT}" -v -s')
    cmd = f'pytest --cov="{PROJECT_ROOT}"'
    getTestOutput =  subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    output = getTestOutput.read().decode()
    return jsonify({'results': output})

def readme(request): # pragma: no cover
    readme = ''
    with open(f"{PROJECT_ROOT}/README.md", "r") as f:
        readme = f.read()
    return jsonify({'results': readme})