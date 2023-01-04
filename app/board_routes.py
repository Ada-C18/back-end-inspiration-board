from flask import Blueprint, request, jsonify, make_response
from .card_routes import validate_model
from app.models.card import Card
from app.models.board import Board
from app import db

board_bp = Blueprint('board_bp', __name__, url_prefix='/boards')




@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if len(request_body) != 2:
        return {"details": "Invalid Data"}, 400
    new_board = Board.from_dict_to_object(request_body)

    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify({"board": new_board.to_dict()}), 201)

@board_bp.route("", methods=["GET"])
def read_all_boards():
    boards = Board.query.all()
    board_response = [board.to_dict() for board in boards]

    return make_response(jsonify(board_response), 200)

@board_bp.route("/<board_id>/cards", methods=["GET"])
def read_all_cards(board_id):
    board = validate_model(Board, board_id)
    boards_response = [card.to_dict() for card in board.cards]
    return(jsonify(boards_response))


@board_bp.route("/<board_id>/cards", methods=["POST"])
def add_card_to_board(board_id):
    request_body = request.get_json()
    if len(request_body) != 1:
        return {"details": "Invalid Data"}, 400
    # new_card = Card.from_dict_to_object(request_body)

    board = validate_model(Board,board_id)
    card_id = request_body["card_id"]
    # board = board.to_dict(cards=True)
    board.cards.append(Card.query.get(card_id))
    
    db.session.commit()

    return make_response(jsonify({'board_id': board.board_id, 'card': [card.message for card in board.cards]}), 200)

    # return make_response(jsonify({"card": new_card.to_dict()}), 201)

# @board_bp.route("/<board_id>/cards", methods=["POST"])
# def add_card_to_board(board_id):

#     board = validate_model(Board, board_id)
#     new_card = create_card()

#     request_body = request.get_json()
#     board.cards += Card.query.get(card_id)

#     db.session.commit()
#     return make_response(jsonify({{'board_id': board.board_id, 'messages': [card.message for card in board.cards]}}))
