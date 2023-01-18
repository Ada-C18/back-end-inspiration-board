from  app import db
from app.models.board import Board
from flask import Blueprint, request, jsonify, make_response
from app.models.card import Card
import os
import requests
from dotenv import load_dotenv

load_dotenv()

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


@boards_bp.route("",  methods=["GET"])
def get_all_boards():
    all_boards = Board.query.all()
    board_titles = [{"owner": board.owner, "title": board.title, "board_id": 
        board.board_id} for board in all_boards]
    return jsonify(board_titles), 200


@boards_bp.route("/<id>",  methods=["GET"])
def get_one_board(id):
    board = Board.query.get(id)
    return {
        'owner': board.owner,
        'title': board.title,
        'id': board.board_id
    }



@boards_bp.route("",  methods=["POST"])
def create_one_board():
    if not request.is_json:
        return {"msg": "Missing JSON request body"}, 400
    request_body = request.get_json()
    try:
        title = request_body["title"]
        owner = request_body["owner"]
    
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    new_board = Board(
        title=title,
        owner=owner
    )

    db.session.add(new_board)
    db.session.commit()
    
    # rsp = {"board": new_board.get_dict()}
    # return jsonify(rsp), 201
    return jsonify(request_body["title"]), 201


# Create
# Create a new card for the selected board, by filling out a form and filling out a "message."
# See an error message if I try to make the card's "message" more than 40 characters.
# All error messages can look like a new section on the screen, a red outline around the input field, and/or disabling the input, as long as it's visible
# See an error message if I try to make a new card with an empty/blank/invalid/missing "message."
@boards_bp.route("/<id>/cards", methods=["POST"])
def create_card_for_specific_board(id):
    board = Board.query.get(id)
    request_body = request.get_json()
    if not request.is_json:
        return {"msg": "Missing JSON request body"}, 400
    try:
        message = request_body["message"]

    except KeyError:
        return {"details": "Invalid message"}, 400

    new_card = Card(
        message=request_body["message"],
        
        )
    # message = new_card.message
    if len(message) > 40:
        return "message more than 40 characters"
    
    db.session.add(new_card)
    board.cards.append(new_card)
    db.session.commit()

    card_info = { 
        "card_id": new_card.card_id,
        "board_id": new_card.board_id,
        "message": new_card.message,
        "likes_count": new_card.likes_count
        }
    
    return jsonify(card_info), 200
    
    
@boards_bp.route("/<id>/cards", methods=["GET"])
def get_cards_from_board(id):
    board = Board.query.get(id)
    if board is None:
        return jsonify(""), 404
    cards = []
    
    for card in board.cards:
        cards.append({
            "card_id": card.card_id,
            "message": card.message,
            "likes_count": card.likes_count
            })
        
    board_info = {
        # "title": board.title,
        # "owner": board.owner,
        "cards": cards,
        "id": board.board_id
    }
    return jsonify(board_info), 200


@boards_bp.route("/<id>", methods=["DELETE"])
def delete_board(id):
    board = Board.query.get(id)
    if board is None:
        return jsonify(""), 404

    db.session.delete(board)
    db.session.commit()

    rsp = {"details": f'Board {id} "{board.title}" successfully deleted'}
    return jsonify(rsp), 200


@boards_bp.route("/<id>", methods=["PUT"])
def update_one_board(id):
    board = Board.query.get(id)

    if not request.is_json:
        return {"msg": "Missing JSON request body"}, 400

    request_body = request.get_json()
    try:
        board.title = request_body["title"]
    except KeyError:
        return {
            "msg": "Update failed due to missing data. Title is required!"
        }, 400

    db.session.commit()
    
    return jsonify(request_body["title"]), 201
    # rsp = {"board": board.get_dict()}
    # return jsonify(rsp), 200