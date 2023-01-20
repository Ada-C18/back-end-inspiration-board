from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

from sqlalchemy.exc import IntegrityError

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


# ____________________________________________________________________________________________________________
# --------------------------------CREATE BOARD-----------------------------------------------------------------
# ____________________________________________________________________________________________________________
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    new_board = Board.from_dict(request_body)
    db.session.add(new_board)
    db.session.commit()

    result = new_board.to_dict()
    return make_response(jsonify(result), 201)


# __________________________________________________________________________________________________________
# -----------------------------------GET BOARD---------------------------------------------------------------
# __________________________________________________________________________________________________________
@boards_bp.route("", methods=["GET"])
def get_boards():
    id_query = request.args.get("board_id")

    if id_query:  # TODO: this seems broken?
        boards = Board.query.order_by(Board.board_id.asc()).all()
    else:
        boards = Board.query.all()

    board_list = [board.to_dict() for board in boards]

    return jsonify(board_list), 200


@boards_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_model(Board, board_id)
    board_dict = board.to_dict()
    return jsonify({"board": board_dict})


@boards_bp.route("/<board_id>/cards", methods=["GET"])
def read_board_cards(board_id):
    board = validate_model(Board, board_id)
    response = [card.to_dict() for card in board.cards]
    return jsonify(response), 200


# __________________________________________________________________________________________________________
# --------------------------------COLOR ROUTES---------------------------------------------------------------
# __________________________________________________________________________________________________________
@boards_bp.route("/<board_id>/color", methods=["GET"])
def get_board_color(board_id):
    board = validate_model(Board, board_id)
    board_dict = board.to_dict(color=True)
    db.session.commit()
    return make_response(jsonify({"board": board_dict}))


@boards_bp.route("/<board_id>/color", methods=["POST"])
def set_board_color(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()
    board.set_color(request_body["color"])
    board_dict = board.to_dict(color=True)
    db.session.commit()
    return make_response(jsonify({"board": board_dict}))


# ____________________________________________________________________________________________________________
# --------------------------------DELETE BOARD----------------------------------------------------------------
# ____________________________________________________________________________________________________________
@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_model(Board, board_id)
    board_dict = board.to_dict()

    for card in board.cards:
        db.session.delete(card)

    db.session.delete(board)
    db.session.commit()

    return jsonify({"message": (f'Board {board_id} {board_dict["title"]} was deleted')})


@boards_bp.errorhandler(IntegrityError)
@boards_bp.errorhandler(ValueError)
def handle_invalid_data(e):
    return make_response({"message": "invalid or incomplete board data"}, 400)
