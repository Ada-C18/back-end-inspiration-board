from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board
from .card_routes import validate_model

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards") 

@boards_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    return jsonify([board.from_instance_to_dict() for board in boards], 200)

@boards_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_model(Board, board_id)
    return jsonify({"board": board.from_instance_to_dict()}, 200)

@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    try: 
        new_board = Board.from_dict_to_instance(request_body)
    except:
        abort(make_response({"details": "invalid data" }, 400))
    db.session.add(new_board)
    db.session.commit()
    return jsonify({"board": new_board.from_instance_to_dict()}, 201)

@boards_bp.route("", methods=["DELETE"])
def delete_all_board():
    boards = Board.query.all()
    for board in boards:
        db.session.delete(board)
        db.session.commit()
    return jsonify({"details": "all boards deleted"}, 200)

@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_one_board(board_id):
    board = validate_model(Board, board_id)
    db.session.delete(board)
    db.session.commit()
    return jsonify({"details": f"board {board.title} has been deleted"}, 200)
