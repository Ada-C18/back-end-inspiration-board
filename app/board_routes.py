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



