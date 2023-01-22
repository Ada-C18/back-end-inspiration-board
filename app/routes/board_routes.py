from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card
from app.routes.routes_helper import validate_model


boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    
    try:
        new_board = Board.from_dict(request_body)
        
    except KeyError:
        return {"details": "Missing Data"}, 400

    db.session.add(new_board)
    db.session.commit()

    return jsonify(new_board.to_dict()), 201
    

# Get ALL Boards
@boards_bp.route("", methods=["GET"])
def read_all_boards():
    
    boards = Board.query.all()
    boards_response = [board.to_dict() for board in boards]

    return jsonify(boards_response)

# Get ONE Board
@boards_bp.route("/<board_id>", methods=["GET"])
def read_one_board(board_id):    
    board = validate_model(Board, board_id)
    
    return board.to_dict()


# Delete a Board
@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_model(Board, board_id)
   
    db.session.delete(board)
    db.session.commit()

    return make_response({"details": f'{board.title} {board.board_id} successfully deleted'})

# --------------------------- NESTED ROUTES ------------------------------

# create a new card to a board by id
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_card_to_board(board_id):   
    board = validate_model(Board, board_id)
    

    request_body = request.get_json()
    try:
        new_card= Card.from_dict(request_body)
        
    except KeyError:
        return {"details": "Missing Data"}, 400
    
    db.session.add(new_card)
    db.session.commit()

    return new_card.to_dict(), 201


# GET all cards by a specific board
@boards_bp.route("<board_id>/cards", methods=["GET"])
def read_all_cards_by_board(board_id):
    board = validate_model(Board, board_id)
    

    cards_response = [card.to_dict() for card in board.cards]

    return jsonify(cards_response)