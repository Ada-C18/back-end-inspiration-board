from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("board", __name__,url_prefix="/boards")
card_bp = Blueprint("card", __name__,url_prefix="/cards")

#GET route for ALL boards
@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    result = []
    for board in boards:
        result.append(board.to_dict())
        # need to create to_dict method in Board Model
    return jsonify(result), 200