from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models import Card, Board
from app.helpers import validate_model
from board_routes import board_bp

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

#Read all cards from board (GET)
@board_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_by_board(board_id):
    board = validate_model(Board, board_id)
    cards_response = [card.to_dict() for card in board.cards]

    return make_response(jsonify(cards_response))

#Add card to board (POST)
@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_card(board_id):
    request_body = request.get_json()
    new_card = Card.from_json(request_body)
    new_card.board_id = board_id

    db.session.add(new_card)
    db.session.commit()
    return make_response(jsonify(new_card.to_dict()), 201)


#Delete card from board (DELETE)
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response(jsonify(f"Card {card_id} deleted"))

#Update card (PUT)
@cards_bp.route("/<card_id>/add_like", methods=["PUT"])
def update_card(card_id):
    card = validate_model(Card, card_id)
    card.likes_count += 1

    db.session.commit()

    return make_response(jsonify(card.to_dict()))
