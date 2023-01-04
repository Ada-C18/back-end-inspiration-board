from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.validate_data import validate_model

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

# #################################
#        CREATE ONE BOARD
# ####################################


@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body or \
            "description" not in request_body:
        return make_response("Invalid Request", 400)

    new_board = Board.from_dict(request_body)

    db.session.add(new_board)
    db.session.commit()

    return jsonify({"board": new_board.to_dict()}), 201

# #####################################
#        GET ALL BOARDS
# #####################################


@boards_bp.route("", methods=["GET"])
def read_all_boards():

    boards = Board.query.all()

    boards_response = []  # returns empty list if no goals

    for board in boards:
        boards_response.append({
            "board_id": board.board_id,
            "title": board.title,
        })

    return jsonify(boards_response), 200
