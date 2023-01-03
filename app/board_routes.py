from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
# example_bp = Blueprint('example_bp', __name__)

board_bp = Blueprint('boards', __name__, url_prefix="/boards")

#Get Routes
@board_bp.route("", methods = ['GET'])
def get_all_boards():

    boards = Board.query.all()

    all_boards = [board.to_dict() for board in boards]

    return jsonify(all_boards)