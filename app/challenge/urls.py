from flask import Blueprint, request
from app.challenge import challenge, views
from flask import current_app, jsonify


@challenge.route("/api/collatz", methods=["POST"])
def collatz_home():
    return views.collatz(request)

@challenge.route("/api/fifth", methods=["POST"])
def fifth():
    return views.fifth(request)

@challenge.route("/api/roman", methods=["POST"])
def roman():
    return views.roman(request)
