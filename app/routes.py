from flask import Blueprint, request, jsonify, make_response
from app.models.board import Board
from app.models.card import Card
from app import db

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint('board_bp', __name__, url_prefix='/board')

"""Board Routes"""
@board_bp.route("", methods=['POST'])
def add_one_board():
    response_body = request.get_json()
    try:
        new_board = Board.create_board(response_body)
    except KeyError:
        return make_response(jsonify({'warning':'invalid title or owner'}),400)
    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify({'msg':f'Board with id {new_board.board_id} created'}),201)