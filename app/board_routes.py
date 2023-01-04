from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
import os, requests

# creating blueprint
board_bp = Blueprint("Board", __name__, url_prefix="/boards")

# Create a board/post
@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    if "title" not in request_body or "owner" not in request_body:
        return make_response({"Details": "Missing title or owner"}, 400)

    new_board = Board.from_dict(request_body)

    db.session.add(new_board)
    db.session.commit()
    response_body = {
        "board": new_board.to_dict()
        }
    return make_response(response_body, 201)

# send a request to create a new card and connect it to a board already found in the database
@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_card_associated_with_board(board_id):
    board = validate_model(Board, board_id)

    request_body = request.get_json()
    new_card = Card(
        board=board,
        message=request_body["message"],
        likes_count=request_body["likes_count"]
    )

    db.session.add(new_card)
    db.session.commit

    # return {"card": new_card.to_dict()}, 201
    return make_response(jsonify(f"Card {new_card.message} on {new_card.board.title} successfully created"), 201)

#send a request to read all cards on a particular board in the database.
@board_bp.route("/<board_id>/cards", methods=["GET"])
def read_all_cards_from_board(board_id):
    board = validate_model(Board, board_id)

    cards_response = []
    for card in board.cards:
        cards_response.append(card.to_dict())
    return jsonify(cards_response)

