from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"Message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"Message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


@board_bp.route("", methods=["GET"])
def get_all_boards():

    boards = Board.query.all()

    boards_response = []
    for board in boards:
        boards_response.append({
            "id": board.board_id,
            "name": board.name,
            "owner": board.owner
        })
    return jsonify(boards_response), 200

@board_bp.route("", methods=["POST"])
def create_board():

    request_body = request.get_json()

    attributes = ["name", "owner"]

    for attribute in attributes:
        if attribute not in request_body or len(request_body[attribute]) == 0:
            abort(make_response({"details": "Invalid data"}, 400))

    new_board = Board(
        name=request_body["name"],
        owner=request_body["owner"]
    )

    db.session.add(new_board)
    db.session.commit()

    return make_response(f"Board {new_board.name} successfully created", 201)
