from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.helpers import validate_model

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("boards", __name__, url_prefix="/boards")


@board_bp.route("/boards", methods=["POST"])
def create_board():
    request_body = request.get_json()

    new_board = Board(title=request_body["title"],
                      owner=request_body["owner"])

    db.session.add(new_board)
    db.session.commit()

    return make_response(f"Board {new_board.title} successfully created", 201)


@board_bp.route("", methods=["GET"])
def get_boards():
    boards_response = []
    for board in boards:
        boards_response.append(
            {
                "id": board.id,
                "title": board.title,
                "owner": board.owner
            }
        )
    return jsonify(boards_response)


@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board_id = int(board_id)
    for board in boards:
        if board.id == board_id:
            return {
                "id": board.id,
                "title": board.title,
                "owner": board.owner,
            }


@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_model(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    return make_response(jsonify(f"Board #{board.id} successfully deleted"))
