from flask import Blueprint, json, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card
from .validation import get_one_obj_or_abort
import requests
import os


boards_bp = Blueprint('boards', __name__, url_prefix='/boards')

@boards_bp.route('', methods=['POST'])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body or "owner" not in request_body:
        return jsonify(
            {"details": "Invalid data"}
        ), 400
    else:
        new_board = Board.from_dict(request_body)
    db.session.add(new_board)
    db.session.commit()
    return jsonify(new_board.to_dict()), 201

@boards_bp.route('', methods=['GET'])
def get_all_boards():
    board_response = []
    boards = Board.query.all()  
    for board in boards:
        board_response.append(board.to_dict())
    return jsonify(board_response), 200

@boards_bp.route('/<board_id>', methods=['GET'])
def get_one_board(board_id):
    chosen_board = get_one_obj_or_abort(Board, board_id)
    return jsonify(chosen_board.to_dict()), 200
    


@boards_bp.route('<board_id>/cards', methods=['POST'])
def add_cards_to_a_board(board_id):
    chosen_board = get_one_obj_or_abort(Board, board_id)
    request_body = request.get_json()

    new_card = Card.from_dict(request_body)
    new_card.board = chosen_board
    
    db.session.add(new_card)
    db.session.commit()
    return jsonify(new_card.to_dict()), 201

@boards_bp.route('<board_id>/cards', methods=['GET'])
def get_all_cards_belongs_to_a_board(board_id):
    
    chosen_board = get_one_obj_or_abort(Board, board_id)
    cards_list = []
    for card in chosen_board.cards:
        cards_list.append(card.to_dict()) 
    return jsonify(cards_list), 200

