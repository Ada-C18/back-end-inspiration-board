from flask import Blueprint, request, jsonify, make_response
from app.helper_func import get_validate_model
from app.models.board import Board
from app.models.card import Card
from app import db

card_bp = Blueprint ("card", __name__, url_prefix= "/cards")


# Read one card
@card_bp.route("/<card_id>", strict_slashes=False, methods=["GET"])
def read_one_card(card_id):
    card = get_validate_model(Card, card_id)

    return make_response(jsonify(card.to_dict()), 200)     # board_id


# Delete Card
@card_bp.route("/<card_id>", strict_slashes=False, methods=["DELETE"])
def delete_card(card_id):
    card = get_validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    response_body = {
        "message": f'Card #{card_id} was deleted.'}
    return make_response(jsonify(response_body), 200)


# Update count of Likes for a Card
@card_bp.route("/<card_id>", strict_slashes=False, methods=["PATCH"])
def update_card(card_id):
    card = get_validate_model(Card, card_id)

    # request_body = request.get_json()
    # card.message = request_body["message"]
    card.likes += 1

    db.session.commit()

    current_card_response = card.to_dict()
    return make_response(jsonify(current_card_response), 200)
