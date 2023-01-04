from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
# example_bp = Blueprint('example_bp', __name__)

board_bp = Blueprint('boards', __name__, url_prefix="/boards")

def validate_model(cls, model_id):
    try:
        model_id=int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__}{model_id} invalid"}, 400))
    model =  cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))
    return model

#Get Routes
@board_bp.route("", methods = ['GET'])
def get_all_boards():

    boards = Board.query.all()

    all_boards = [board.to_dict() for board in boards]

    return jsonify(all_boards)

@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_model(Board, board_id)
    return {"board": board.to_dict()}, 200


