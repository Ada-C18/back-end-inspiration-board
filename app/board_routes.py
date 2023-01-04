from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from .models.board import Board
from .models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint('boards_bp', __name__, url_prefix="/boards")
# create a board
@boards_bp.route("", methods =["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body or "owner" not in request_body:
        return jsonify({"details":"Invalid data"}), 400
    
    new_board = Board (
        title=request_body["title"],
        owner=request_body["owner"])
    db.session.add(new_board)
    db.session.commit()
    return jsonify({new_board.to_dict_board()}), 201