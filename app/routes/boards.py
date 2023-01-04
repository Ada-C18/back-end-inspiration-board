from flask import Blueprint, json, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from .validation import get_board_from_id
import requests
import os


boards_bp = Blueprint('boards', __name__, url_prefix='/boards')

@boards_bp.route('', methods=['POST'])
def create_board():
    request_body = request.get_json()
    if "title" and "owner" not in request_body:
        return jsonify(
            {"details": "Invalid data"}
        ), 400
    new_board = Board.from_dict(request_body)
    db.session.add(new_board)
    db.session.commit()
    return jsonify({"board": new_board.to_dict()}), 201


@boards_bp.route('', methods=['GET'])
def get_all_boards():
    board_response = []
    boards = Board.query.all()  
    for board in boards:
        board_response.append(board.to_dict())
    return jsonify(board_response), 200

@boards_bp.route('/<board_id>', methods=['GET'])
def get_one_board(board_id):
    chosen_board = get_board_from_id(board_id)
    return jsonify(chosen_board.to_dict()), 200
    