from flask import Blueprint, request, jsonify, make_response,abort
from app import db
from app.models.board import Board
from app.models.card import Card


board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")

def validate_board_id(board_id):
    try:
        board_id = int(board_id)
    except ValueError:
        abort(make_response(jsonify({"message": "board_id must be an integer"}),400))
    
    matching_board = Board.query.get(board_id)

    if matching_board is None:
        response_str = f"Board with id {board_id} was not found in the database."
        abort(make_response(jsonify({"message": response_str}), 404))

    return matching_board


@board_bp.route("", methods = ["POST"])
def add_board():
    request_body = request.get_json()
    if "title" not in request_body or "owner" not in request_body:
        return jsonify({"details": "Invalid data"}),400

    new_board = Board(title=request_body["title"],owner=request_body["owner"])


    db.session.add(new_board)
    db.session.commit()

    board_dict = new_board.to_dict()

    return jsonify(board_dict),201

@board_bp.route("", methods=["GET"])
def get_all_boards():

    boards = Board.query.all()
    
    response = [board.to_dict() for board in boards]

    return jsonify(response), 200

@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_board_id(board_id)

    board_dict = board.get_cards()

    return jsonify(board_dict), 200



