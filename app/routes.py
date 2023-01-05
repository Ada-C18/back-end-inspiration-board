from flask import abort, Blueprint, request, jsonify, make_response
from app import db
import os, requests
from dotenv import load_dotenv

from app.models.board import Board
from app.models.card import Card

# board
board_bp = Blueprint("boards", __name__, url_prefix="/boards")

@board_bp.route('', methods=['GET'])
def get_all_boards():
    boards = Board.query.all()

    result = []
    for item in boards:
        result.append(item.to_dict())

    return jsonify(result), 200

@board_bp.route('/<board_id>', methods=['GET'])
def get_one_board(board_id):
    chosen_board = get_model_from_id(Board, board_id) 
    return jsonify({"board": chosen_board.to_dict()}), 200

@board_bp.route('', methods=['POST'])
def create_one_board():
    request_body = request.get_json()

    try:
        new_board = Board(title = request_body["title"], owner = request_body["owner"])
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_board)
    db.session.commit()

    return jsonify({"board": new_board.to_dict()}), 201

@board_bp.route('/<board_id>', methods=['PUT'])
def update_one_board(board_id):
    update_board = get_model_from_id(Board, board_id)

    request_body = request.get_json()

    try:
        update_board.title = request_body["title"]
        update_board.owner = request_body["owner"]
    except KeyError:
        return jsonify({"msg": "Missing needed data"}), 400

    db.session.commit()
    return jsonify({"board": update_board.to_dict()}), 200

@board_bp.route('/<board_id>', methods=['DELETE'])
def delete_one_board(board_id):
    board_to_delete = get_model_from_id(Board, board_id)

    db.session.delete(board_to_delete)
    db.session.commit()

    return jsonify({"details": f'Board {board_to_delete.board_id} {board_to_delete.title} successfully deleted'}), 200 


# card
card_bp = Blueprint("cards", __name__, url_prefix="/cards")

@card_bp.route('', methods=['GET'])
def get_all_cards():
    cards = Card.query.all()

    result = []
    for item in cards:
        result.append(item.to_dict())

    return jsonify(result), 200
    
@card_bp.route('/<card_id>', methods=['GET'])
def get_one_card(card_id):
    chosen_card = get_model_from_id(Card, card_id) 
    return jsonify({"card": chosen_card.to_dict()}), 200

@card_bp.route('', methods=['POST'])
def create_one_card():
    request_body = request.get_json()

    try:
        new_card = Card(message = request_body["message"], like_count = request_body["like_count"])
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_card)
    db.session.commit()

    return jsonify({"card": new_card.to_dict()}), 201

@card_bp.route('/<card_id>', methods=['PUT'])
def update_one_card(card_id):
    update_card = get_model_from_id(Card, card_id)

    request_body = request.get_json()

    try:
        update_card.message = request_body["message"]
        update_card.like_count = request_body["like_count"]
    except KeyError:
        return jsonify({"msg": "Missing needed data"}), 400

    db.session.commit()
    return jsonify({"card": update_card.to_dict()}), 200

@card_bp.route('/<card_id>', methods=['DELETE'])
def delete_one_card(card_id):
    card_to_delete = get_model_from_id(Card, card_id)

    db.session.delete(card_to_delete)
    db.session.commit()

    return jsonify({"details": f'Card {card_to_delete.card_id} successfully deleted'}), 200

# card + board
@board_bp.route('/<board_id>/cards', methods=['GET'])
def get_cards_for_board(board_id):
    chosen_board = get_model_from_id(Board, board_id)

    return jsonify(chosen_board.to_dict_card())

@board_bp.route('/<board_id>/cards', methods=['POST'])
def create_cards_for_board(board_id):
    matching_board = Board.query.get(board_id)

    request_body = request.get_json()
    cards_ids = request_body["cards_ids"]

    cards = matching_board.get_card_list()

    boards_cards_id = [x["id"] for x in cards]

    for cid in cards_ids:
        if cid not in boards_cards_id:
            new_card = Card(message="", like_count=0, board_id=matching_board.board_id)

            db.session.add(new_card)
            db.session.commit()

    return jsonify({"id":matching_board.board_id, "cards_ids":cards_ids}), 200


# helper function
def get_model_from_id(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        return abort(make_response({"msg": f"invalid data: {model_id}"}, 400))

    chosen_model = cls.query.get(model_id)

    if chosen_model is None:
        return abort(make_response({"msg": f"Could not find item with id: {model_id}"}, 404))
    
    return chosen_model

