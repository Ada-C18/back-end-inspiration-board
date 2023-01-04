from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card
import os, requests

# creating blueprint
board_bp = Blueprint("Board", __name__, url_prefix="/boards")

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
    db.session.commit()

    # return {"card": new_card.to_dict()}, 201
    return make_response(jsonify(f"Card {new_card.message} on {new_card.board.title} successfully created"), new_card.to_dict(), 201)

#send a request to read all cards on a particular board in the database.
@board_bp.route("/<board_id>/cards", methods=["GET"])
def read_all_cards_from_board(board_id):
    board = validate_model(Board, board_id)


    cards_response = []
    for card in board.cards:
        cards_response.append(card.to_dict())
    return jsonify(cards_response)

#send a request to read all cards on a particular board in the database.
@board_bp.route("/<board_id>/cards/<card_id>", methods=["PUT"])
def update_card(board_id, card_id):
    board = validate_model(Board, board_id)
    card = validate_model(Card, card_id)

    request_body = request.get_json()

    card.message = request_body["message"]
    card.likes_count = request_body["likes_count"] + 1

    db.session.commit()

    return make_response(jsonify(f"Card {card.card_id} on {board.title} successfully updated"), 200)

# send a request to delete a card from a particular board in the database
@board_bp.route("/<board_id>/cards/<card_id>", methods=["DELETE"])
def delete_card(board_id, card_id):
    board = validate_model(Board, board_id)
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    # return {"details": f'Card {card.id} "{card.message}" successfully deleted'}
    return make_response(jsonify(f"Card {card.card_id} on {board.title} successfully deleted"), 200)


# READ ALL BOARDS/ GET

@board_bp.route("", methods=["GET"])
def get_all_boards():
    response = []
    boards = Board.query.all()
    for board in boards:
        response.append(board.to_dict())
    return jsonify(response)
    # return response.to_dict()

# READ ONE BOARD/ GET
@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):

    board = validate_model(Board, board_id)
    # if board.card_id is None:
    #     return {"board": board.to_dict()}
    # else:
    return {"board": board.to_dict()}

# UPDATE BOARD/ PUT
@board_bp.route("/<board_id>", methods=["PUT"])
def update_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json() 
    board.title = request_body["title"]
    board.owner = request_body["owner"]

    db.session.commit()
    response_body =  {
        "board": board.to_dict()
        }
    return make_response(response_body, 200)

# DELETE BOARD/ DELETE
@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_one_board(board_id):

    board = validate_model(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    return {
        "details": f'Board {board_id} successfully deleted'}
