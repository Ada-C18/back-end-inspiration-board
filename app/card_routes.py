from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# example_bp = Blueprint('example_bp', __name__)
card_bp = Blueprint("cards", __name__, url_prefix="/cards")

def validate_card_id(card_id):
    try:
        card_id = int(card_id)
    except:
        abort(make_response({"message": f"card {card_id} invalid"}, 400))

    card = Card.query.get(card_id)
    if not card:
        abort(make_response({"message": f"card {card_id} not found"}, 404))
    else:
        return card


@card_bp.route("", methods=["GET"])
def get_all_cards():
    cards = Card.query.all()
    all_cards = [card.to_dict() for card in cards]
    return jsonify(all_cards), 200


@card_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    card = validate_card_id(card_id)
    return {"card": card.to_dict()}


@card_bp.route("/<card_id>", methods=["PUT"])
def update_card(card_id):
    card = validate_card_id(card_id)
    request_body = request.get_json()

    card.message = request_body["message"]

    db.session.commit()

    return make_response({"card": card.to_dict()}, 200)


@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_card_id(card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response({"details": f'Card {card_id} "{card.message}" successfully deleted'}, 200)


@card_bp.route("/<card_id>/likes", methods=["PUT"])
def update_card_likes(card_id):
    print(card_id)
    card = validate_card_id(card_id)
    
    request_body = request.get_json()

    card.likes_count = request_body["likes_count"]

    db.session.commit()

    return make_response({"card": card.to_dict()}, 200)