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


