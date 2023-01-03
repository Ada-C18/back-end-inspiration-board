from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card


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

@board_bp.route("", methods=["POST"])
def create_board():
    response_body = request.get_json()
    
    new_board = Board.from_dict(response_body)
    db.session.add(new_board)
    db.session.commit()

    return {"board_id": new_board.board_id}, 201

# @task_bp.route("", methods=["GET"])
# def get_all_tasks():