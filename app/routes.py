from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

boards_bp = Blueprint('boards_bp',__name__, url_prefix ='/boards')

# return all boards
@boards_bp.route("", methods=["GET"])
def get_boards():
    boards = Board.query.all()
    response = [board.to_dict() for board in boards]
    return jsonify(response), 200

# return all cards of a board
@boards_bp.route("/<id>/cards", methods=["GET"])
def get_cards(id):
    board = Board.query.get(id)
    response = [card.to_dict() for card in board.cards]
    return jsonify(response), 200

# increment like count for a card
@boards_bp.route("/<id>/cards/<card_id>", methods=["PATCH"])
def increment_like_count(card_id):
    card = Card.query.get(card_id)
    card.like_count += 1

    db.session.commit()

    return {"message": "likes incremented successfully"}, 200