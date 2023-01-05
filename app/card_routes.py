from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import card

card_bp = Blueprint('card_bp', __name__, url_prefix='/card')


