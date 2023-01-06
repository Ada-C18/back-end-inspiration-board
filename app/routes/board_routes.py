from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

# Create a New Board -> post method

@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    
    try:
        new_board = Board.from_dict(request_body)
        # new_board = Board(
        #     title=request_body["title"],
        #     owner=request_body["owner"]
        # )
    except KeyError:
        return {"details": "Missing Data"}, 400

    db.session.add(new_board)
    db.session.commit()

    return jsonify(new_board.to_dict()), 201
    # return {
    #     "board" : {
    #         "id": new_board.board_id,
    #         "title": new_board.title,
    #         "owner": new_board.owner
    #     }
    # }, 201

# Get ALL Boards
@boards_bp.route("", methods=["GET"])
def read_all_boards():
    # we might need to order because of the way they're listed in the boards
    # cards = Board.query.order_by(Board.board_id).all()
    boards = Board.query.all()
    boards_response = [board.to_dict() for board in boards]

    # for board in boards:
    #     boards_response.append(
    #         {
    #         "id": board.board_id,
    #         "title": board.title,
    #         "owner": board.owner
    #         }
    #     )
    return jsonify(boards_response)

# validate board helper function
def validate_board(board_id):
    try:
        board_id = int(board_id)
    except:
        abort(make_response({"details": "Invalid Data, id must be a number"}, 400))
    
    board = Board.query.get(board_id)
    if not board:
        abort(make_response({"details": f"There is no existing board {board_id}"}, 400))
    
    return board

# Get ONE Board
@boards_bp.route("/<board_id>", methods=["GET"])
def read_one_board(board_id):    
    board = validate_board(board_id)

    return board.to_dict()

    # return {
    #     "board" : {
    #         "id": board.board_id,
    #         "title": board.title,
    #         "owner": board.owner
    #     }
    # }

# Delete a Board
@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_board(board_id)

    db.session.delete(board)
    db.session.commit()

    # return {
    #     "details": f'Board {board.title} owned by {board.owner} successfully deleted'
    # }
    return {
        "details": f'Board {board.title} successfully deleted'
    }

# --------------------------- NESTED ROUTES ------------------------------

# create a new card to a board by id

@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_card_to_board(board_id):   

    board = validate_board(board_id)

    request_body = request.get_json()
    try:
        new_card= Card.from_dict(request_body)
        # new_card = Card(
        #     message=request_body["message"],
        #     likes_count=request_body["likes_count"],
        #     board=board
        # )
    except KeyError:
        return {"details": "Missing Data"}, 400
    
    db.session.add(new_card)
    db.session.commit()

    return new_card.to_dict(), 201

    # return {
    #     "card" : {
    #         "id": new_card.card_id,
    #         "message": new_card.message,
    #         "likes_count": new_card.likes_count,
    #         "board_id": new_card.board_id
    #     }
    # }, 201

# GET all cards by a specific board
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def read_all_cards_by_board(board_id):

    board = validate_board(board_id)

    cards_response = [card.to_dict() for card in board.cards]

    # for card in board.cards:
    #     cards_response.append(
    #         {
    #             "id": card.card_id,
    #             "message": card.message,
    #             "likes_count": card.likes_count,
    #             "board_id": card.board_id
    #         }
    #     )
    return jsonify(cards_response)