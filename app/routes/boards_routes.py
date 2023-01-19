from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
from .helper_routes import validate, validate_board

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["POST"])
def create_boards():
    request_body = request.get_json()
    if "title" not in request_body or "owner" not in request_body:
        return make_response({"details":"data not in request body"},400)
    
    new_boards = Board.from_dict(request_body)
    validate_board(new_boards)
    
    db.session.add(new_boards)
    db.session.commit()

    response = {"boards": new_boards.to_dict()}

    return make_response(jsonify(response)), 201

@boards_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()

    board_response = [board.to_dict() for board in boards]

    return jsonify(board_response), 200

@boards_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate(Board,board_id)

    return {"boards" : board.to_dict()}, 200

@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_board_cards(board_id):
    board = validate(Board,board_id)

    cards = Card.query.filter(Card.board_id == board.board_id)
    cards_response = [card.to_dict() for card in cards]

    return jsonify(cards_response), 200


@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_boards(board_id):
    board = validate(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    return jsonify({"details": f'Board {board_id} "{board.title}"successfully deleted'}), 200






    





