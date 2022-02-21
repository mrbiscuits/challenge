import time
from flask import render_template, redirect, session, current_app, jsonify, request, json, flash
from flask import current_app, flash
from datetime import datetime, timedelta
from flask import abort, jsonify
from app.challenge.fifth import fifth_interpreter
from app.challenge.roman import digitise_numerals
from app.challenge.collatz import collatz_input 

def fifth(request):
    if request.method == 'POST':
        post_data = request.json
        print(post_data)
        results = fifth_interpreter(post_data['stack'], post_data['cmd'], "api")
        return jsonify(results)

def roman(request):
    if request.method == 'POST':
        post_data = request.json
        print(post_data)
        results = digitise_numerals(post_data['cmd'].strip('ROMAN').strip(), "api")
        stack = results['results']+post_data['stack']
        return jsonify({'stack':stack, 'cmd':post_data['cmd'], 'error': results.get("error", 0)})

def collatz(request):
    if request.method == 'POST':
        post_data = request.json
        results = collatz_input(post_data['cmd'].strip('COLLATZ').strip(), caller="api")
        stack = post_data['stack']
        if results.get('steps'):
            stack = [results.get('steps')] + post_data['stack']
        return jsonify({'stack':stack, 'cmd':post_data['cmd'], 'error': results.get("error", 0)})
