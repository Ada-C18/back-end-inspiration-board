from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board

boards_bp = Blueprint('boards_bp', __name__, url_prefix='/boards')

@boards_bp.route('', methods=['GET'])
def get_all_boards():
    boards = Board.query.all()
    board_response = []
    for board in boards:
        board_response.append(
            {
                "id": board.id,
                "title": board.title,
                "owner": board.owner,
                "cards": board.cards,
            }
        )
    return jsonify(board_response)
