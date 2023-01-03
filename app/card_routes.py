from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.validate_data import validate_model


cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


