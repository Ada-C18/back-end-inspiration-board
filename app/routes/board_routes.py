from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

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

# #GET endpoint to get cards for one board
@boards_bp.route("/<board_id>/cards", methods = ["GET"])
def get_board_cards(board_id):
    board = Board.query.get(board_id)
    cards_response = []
    for card in board.cards:
        cards_response.append(
            {"id": card.card_id,
            "message": card.message})
    return jsonify(cards_response)

# POST create a new board
@boards_bp.route("", methods = ["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body or "owner" not in request_body:
        return jsonify({"message": "Title and Owner must be specified."}, 400)
    new_board = Board(
        title = request_body["title"],
        owner = request_body["owner"],
    )

    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify({"board": new_board.title, "owner": new_board.owner}), 201)

# POST create new card
@boards_bp.route("/<board_id>/cards", methods = ["POST"])
def create_card(board_id):
    # board = Board.query.get(board_id)
    request_body = request.get_json()
    
    if "message" not in request_body:
        return jsonify({"message": "Message cannot be blank!"}, 400)
    if len(request_body["message"]) > 40:
        return jsonify({"message": "Maximum length 40 characters."}, 400)

    new_card = Card(
        board_id = board_id,
        message = request_body["message"],
        likes_count = 0
    )

    db.session.add(new_card)
    db.session.commit()
    
    return make_response(jsonify({"card": new_card.message}), 201)

# DELETE route
@boards_bp.route("/<board_id>", methods = ["DELETE"])
def delete_board(board_id):
    board = Board.query.get(board_id)
    db.session.delete(board)
    db.session.commit()

    return make_response(jsonify({"msg": "board successfully deleted"}), 200)