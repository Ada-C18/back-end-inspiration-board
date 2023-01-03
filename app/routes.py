from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

board_bp = Blueprint("board", __name__, url_prefix = "/board")

@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()

    result = []
    for item in boards:
        result.append(item.to_dict())
