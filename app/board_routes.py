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
    board_titles = [{board.owner, board.title, board.board_id} for board in all_boards]
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



@boards_bp.route("/<id>/cards", methods=["POST"])
def create_card_for_specific_board(id):
    board = Board.query.get(id)
    request_body = request.get_json()

    card_ids = request_body["card_ids"]

    for card_id in card_ids:
        card = Card.query.get(card_id)
        if card_id not in board.cards:
            card.board = board

    db.session.commit()

    rsp = {"id": board.board_id, "card_ids": card_ids}
    return jsonify(rsp), 200  

    
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
        "title": board.title,
        "owner": board.owner,
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