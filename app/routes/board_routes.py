from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card
from app.routes.routes_helper import get_one_obj_or_abort

board_bp = Blueprint("board", __name__, url_prefix = "/board")

@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()

    result = []
    for item in boards:
        result.append(item.to_dict())

    return jsonify(result)

@board_bp.route("", methods=["POST"])
def add_board():
    request_body = request.get_json()

    new_board = Board.from_dict(request_body)
    db.session.add(new_board)
    db.session.commit()

    return {"message": f"Successfully created new board with id = {new_board.board_id}"}, 201

@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    chosen_board = get_one_obj_or_abort(Board, board_id)

    board_dict = chosen_board.to_dict()

    return jsonify(board_dict), 200


@board_bp.route("/<board_id>/card", methods=["POST"])
def post_card_belonging_to_a_board(board_id):
    parent_board = get_one_obj_or_abort(Board, board_id)

    request_body = request.get_json()

    new_card = Card.from_dict(request_body)
    new_card.board = parent_board

    db.session.add(new_card)
    db.session.commit()

    return jsonify({"message":f"Card {new_card.message} belonging to {new_card.board.title} successfully added"}), 201

# get all cards belonging to a board
@board_bp.route("/<board_id>/card", methods=["GET"]) 
def get_all_cards_belonging_to_a_board(board_id):
    board = get_one_obj_or_abort(Board, board_id)
    
    cards_response = [card.to_dict() for card in board.cards]

    return jsonify(cards_response), 200
    

