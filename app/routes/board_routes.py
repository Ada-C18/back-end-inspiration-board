from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

# from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix = "/boards")

# GET endpoint to get all boards
@boards_bp.route("", methods = ["GET"])
def get_all_boards():
    boards = Board.query.all()
    boards_response = []
    for board in boards:
        boards_response.append(
            {
              "board_id": board.board_id,
              "title": board.title,
              "owner": board.owner  
            }
        )
    return jsonify(boards_response)

# POST create a new board
@boards_bp.route("", methods = ["POST"])
def create_board():
    request_body = request.get_json()
    new_board = Board(
        title = request_body["title"],
        owner = request_body["owner"],
    )

    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify({"board": new_board.title, "owner": new_board.owner}), 201)