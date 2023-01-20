from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.card import Card

from sqlalchemy.exc import IntegrityError

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# ==================================
# Helper function to validate id
# ==================================
def validate_id(class_name, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"Id {id} is an invalid id"}, 400))

    query_result = class_name.query.get(id)
    if not query_result:
        abort(make_response({"message": f"Id {id} not found"}, 404))

    return query_result


# ==================================
# CREATE CARD
# ==================================
@cards_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()

    new_card = Card.from_dict(request_body)
    db.session.add(new_card)
    db.session.commit()

    result = new_card.to_dict()
    return make_response(jsonify({"card": result}), 201)


# ==================================
# GET  CARD
# ==================================
@cards_bp.route("", methods=["GET"])
def get_cards():
    cards = Card.query.all()
    cards_response = [card.to_dict() for card in cards]

    return jsonify(cards_response), 200


@cards_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    card = validate_id(Card, card_id)
    card_dict = card.to_dict()

    return jsonify({"card": card_dict})


# ==================================
# DELETE one card by id
# ==================================
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    card = validate_id(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response({"message": f"Card {card.card_id} successfully deleted"}, 200)


# ==================================
# PATCH one card by id
# ==================================
@cards_bp.route("<card_id>", methods=["PATCH"])
def edit_card_likes(card_id):
    card = validate_id(Card, card_id)
    card.likes_count += 1
    db.session.commit()
    return jsonify(card.to_dict()), 200


@cards_bp.errorhandler(IntegrityError)
@cards_bp.errorhandler(KeyError)
def handle_invalid_data(e):
    return make_response({"message": "Invalid or incomplete card data"}, 400)
