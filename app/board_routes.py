from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card
import os, requests

# creating blueprint
board_bp = Blueprint("Board", __name__, url_prefix="/boards")

# CREATE BOARD/POST
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

# READ ALL BOARDS/ GET

@board_bp.route("", methods=["GET"])
def get_all_boards():
    response = []

    for board in board:
        response.append(board.to_dict())
    return jsonify(response)
    # return response.to_dict()

# READ ONE BOARD/ GET
@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):

    board = validate_model(Board, board_id)
    if board.card_id is None:
        return {"board": board.to_dict()}
    else:
        return {"board": board.to_new_dict()}

# UPDATE BOARD/ PUT
# UPDATE BOARD/ PATCH
# DELETE BOARD/ DELETE

#VALIDATE MODEL
def validate_model(class_obj,id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"{id} is an invalid id"}, 400))
    query_result = class_obj.query.get(id)
    if not query_result:
        abort(make_response({"message":f"{id} not found"}, 404))

    return query_result



