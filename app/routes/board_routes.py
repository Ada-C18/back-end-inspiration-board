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

#GET endpoint to get one board
@boards_bp.route("/<board_id>", methods = ["GET"])
def get_one_board(board_id):
    board = Board.query.get(board_id)
    return make_response(jsonify(
        {
              "board_id": board.board_id,
              "title": board.title,
              "owner": board.owner  
            }
    ), 200)

#GET endpoint to get cards for one board
@boards_bp.route("/<board_id>/cards", methods = ["GET"])
def get_board_cards(board_id):
    board = Board.query.get(board_id)
    cards_response = []
    for card in board.cards:
        cards_response.append(card)
    return make_response(jsonify(
        cards_response
    ), 200)

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

# DELETE route
@boards_bp.route("/<board_id>", methods = ["DELETE"])
def delete_board(board_id):
    board = Board.query.get(board_id)
    db.session.delete(board)
    db.session.commit()

    return make_response(jsonify({"msg": "board successfully deleted"}), 200)