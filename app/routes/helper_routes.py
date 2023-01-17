from flask import jsonify, abort, make_response
from app.models.board import Board

from app.models.card import Card

def validate(cls,obj_id):
    try:
        obj_id = int(obj_id)
    except ValueError:
        abort(make_response(jsonify({"message":"details: invalid data"}), 400))

    matching_obj = cls.query.get(obj_id)

    if not matching_obj:
        response_str = f"{cls.__name__.lower()} not found"
        abort(make_response(jsonify({"message":response_str}), 404))

    return matching_obj

def validate_card(card: Card):
    msg_len = len(card.message)
    if msg_len <1 or msg_len > 40:
        abort(make_response(jsonify({"message": "details: invalid data"}), 400))

def validate_board(board: Board):
    title_len = len(board.title)
    owner_len = len(board.owner)
    if title_len<1 or owner_len < 1:
        abort(make_response(jsonify({"message": "details: invalid data"}), 400))
