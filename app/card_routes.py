from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card


cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")
def validate_cards(card_id):
    try:
        card_id = int(card_id)
    except:
        abort(make_response({"details": f"{card_id}: invalid data"}, 400))
    card = Card.query.get(card_id)
    if not card:
        abort(make_response({"message": f"card {card_id} not found"}, 404))
    return card