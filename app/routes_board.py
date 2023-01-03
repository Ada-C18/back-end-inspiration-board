from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board


boards_bp = Blueprint('boards_bp', __name__, url_prefix="/boards")

# Helper function
def get_model_from_id(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        return abort(make_response({"msg": f"invalid data type: {model_id}"}, 200))


    chosen_model = cls.query.get(model_id)

    if chosen_model is None:
        return abort(make_response({"msg": f"Could not find model with id: {model_id}"}, 404))

    return chosen_model

@boards_bp.route("", methods=['POST'])
def post_a_board():
    request_body=request.get_json()

    try:
        new_board=Board.from_dict(request_body)
        db.session.add(new_board)
        db.session.commit()
    except KeyError:
        return jsonify({"msg": "Invalid Data"}), 400

    return jsonify({"board": new_board.to_dict()}), 201

@boards_bp.route("/<board_id>", methods=['GET'])
def get_one_board(board_id):
    chosen_board= get_model_from_id(Board, board_id)

    return jsonify({"board": chosen_board.to_dict()}), 200

@boards_bp.route("", methods=["GET"])
def get_all_board():
    all_boards = Board.query.all()
    all_boards_response=[board.to_dict() for board in all_boards]

    return jsonify(all_boards_response), 200

@boards_bp.route("<board_id>", methods=["DELETE"])
def delete_one_board(board_id):
    board_to_delete = get_model_from_id(Board, board_id)
    title_board_to_delete = get_model_from_id(Board, board_id).to_dict()["title"]

    db.session.delete(board_to_delete)
    db.session.commit()
    return jsonify({"msg": f"board {board_id} '{title_board_to_delete}' deleted"}), 200