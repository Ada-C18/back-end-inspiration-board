from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board
import os, requests
from app.board_routes import validate_model

# Card
# CREATE a new card to a board (in board_routes)
# READ all cards belonging to a board (in board_routes)
# UPDATE ‘+1’s for a card
# DELETE a card


# creating blueprint
card_bp = Blueprint("Card", __name__, url_prefix="/cards")

#send a request to read all cards on a particular board in the database.
@card_bp.route("/<card_id>/like", methods=["PUT"])
def update_card( card_id):
    card = validate_model(Card, card_id)

    request_body = request.get_json()

    card.message = request_body["message"]
    card.likes_count = request_body["likes_count"] + 1

    db.session.commit()

    return card.to_dict(), 200
    # return make_response(jsonify(f"Card {card.card_id} on {board.title} successfully updated"), 200)


# send a request to delete a card from a particular board in the database
@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return {"details": f'Card {card.card_id} successfully deleted")'}
    # return make_response(jsonify(f"Card {card.card_id} on {board.title} successfully deleted"), 200)
