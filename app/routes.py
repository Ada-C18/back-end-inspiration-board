from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)

cards_bp = Blueprint("cards",__name__, url_prefix="/cards")

@cards_bp.route("", methods=["POST"])
def handle_cards():
    request_body = request.get_json()
    new_card = Card(message= request_body["message"])

    db.session.add(new_card)
    db.session.commit()

    return make_response(f"Card {new_card.message} successfully created", 201)