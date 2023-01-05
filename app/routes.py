from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
from .routes_helper import get_one_obj_or_abort


# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")
card_bp = Blueprint("card_bp", __name__, url_prefix="/cards")

@card_bp.route("", methods=["POST"])
def create_card():
    response_body = request.get_json()
    
    new_card = Card.from_dict(response_body)
    db.session.add(new_card)
    db.session.commit()

    return {"card_id": new_card.card_id}, 201

@card_bp.route("", methods=["GET"])
def get_all_cards():
    
    cards = Card.query.order_by(Card.card_id).all()
    response = [card.to_dict() for card in cards]

    return jsonify(response), 200



@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_bike(card_id):
    chosen_card = get_one_obj_or_abort(Card, card_id)

    db.session.delete(chosen_card)

    db.session.commit()

    return jsonify({"message": f"Successfully deleted card with id `{card_id}`"}), 200

 ####################
@board_bp.route("", methods=["POST"])
def create_board():
    response_body = request.get_json()
    
    new_board = Board.from_dict(response_body)
    db.session.add(new_board)
    db.session.commit()

    return {"board_id": new_board.board_id}, 201

# @task_bp.route("", methods=["GET"])
# def get_all_tasks():
@board_bp.route("", methods=["GET"])
def get_all_boards():
   
    boards = Board.query.order_by(Board.board_id).all()
    response = [board.to_dict() for board in boards]

    return jsonify(response), 200


@board_bp.route("/<board_id>/card", methods=["GET"])
def get_all_cards_belong_to_a_board(board_id):
    board = get_one_obj_or_abort(Board, board_id)

    card_response = [card.to_dict() for card in board.cards]

    return jsonify(card_response), 200


# @board_bp.route("/boards", methods=["DELETE"])
# def delete_board(board_id):
#     chosen_board = get_one_obj_or_abort(Board, board_id)

#     db.session.delete(chosen_board)

#     db.session.commit()

#     return jsonify({"message": f"Successfully deleted board with id `{board_id}`"}), 200

@board_bp.route("/<board_id>/card", methods=["POST"])
def post_card_belonging_to_a_board(board_id):
    parent_board = get_one_obj_or_abort(Board, board_id)

    request_body = request.get_json()

    new_card = Card.from_dict(request_body)
    new_card.board = parent_board

    db.session.add(new_card)
    db.session.commit()

    return jsonify({"message":f"Card {new_card.message} belonging to {new_card.board.title} successfully added"}), 201
