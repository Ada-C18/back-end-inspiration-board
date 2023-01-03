from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card


cards_bp = Blueprint('cards_bp', __name__, url_prefix = '/cards')
# example_bp = Blueprint('example_bp', __name__)
