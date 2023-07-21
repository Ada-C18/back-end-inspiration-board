from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card
from app.helpers import validate_model

board_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

### CREATE ROUTES ###

#Create a new board
@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    new_board = Board.from_json(request_body)

    if len(new_board.title) == 0:
        abort(make_response(jsonify({'error': 'Board must have a title'}), 404))
    if len(new_board.owner) == 0:
        abort(make_response(jsonify({'error':'Board must have an owner'}), 404))

    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify(new_board.to_dict()), 201)

#Add a card to a board
@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_card(board_id):
    request_body = request.get_json()
    new_card = Card.from_json(request_body)

    if len(new_card.message) > 40:
        abort(make_response(jsonify({'error':"Card message cannot exceed 40 characters"}), 404))
    if len(new_card.message) == 0:
        abort(make_response(jsonify({'error': 'Card message cannot be empty'}), 404))

    board = validate_model(Board, board_id)
    new_card.board_id = board.board_id

    db.session.add(new_card)
    db.session.commit()
    return make_response(jsonify(new_card.to_dict()), 201)

### READ ROUTES ###

#Read all boards
@board_bp.route("", methods=["GET"])
def get_boards():
    boards_response = []
    for board in Board.query.all():
        boards_response.append(board.to_dict())
    return jsonify(boards_response)

#Read one board by ID
@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_model(Board, board_id)
    return jsonify(board.to_dict())

#Read all cards from a board
@board_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_by_board(board_id):
    board = validate_model(Board, board_id)
    cards_response = [card.to_dict() for card in board.cards]

    return make_response(jsonify(cards_response))

#Read all cards
@cards_bp.route("", methods=["GET"])
def get_cards():
    cards = Card.query.all()
    cards_response = [card.to_dict() for card in cards]

    return make_response(jsonify(cards_response))

### UPDATE ROUTES ###

#Update likes of card
@cards_bp.route("/<card_id>/add_like", methods=["PUT"])
def update_card(card_id):
    card = validate_model(Card, card_id)
    card.likes_count += 1

    db.session.commit()

    return make_response(jsonify(card.to_dict()))

### DELETE ROUTES ###

#Delete board
@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_model(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    return make_response(jsonify(f"Board #{board.board_id} successfully deleted"))

#Delete card
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response(jsonify(f"Card {card_id} deleted"))

