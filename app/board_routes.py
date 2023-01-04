from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.validate_data import validate_model

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


#===================================
#        READ ONE BOARD BY ID
#===================================

@boards_bp.route("/<board_id>", methods=["GET"])
def read_one_board(board_id):
    board = validate_model(Board, board_id)
    response_one_board = {"board": Board.to_dict(board)}
    return jsonify(response_one_board), 200