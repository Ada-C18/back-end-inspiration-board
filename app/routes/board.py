from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board

bp = Blueprint("board_bp", __name__, url_prefix="/boards")


@bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    check_duplicates(request_body["title"])

    new_board = Board.from_dict(request_body)

    db.session.add(new_board)
    db.session.commit()

    board_dict = new_board.to_dict()

    return make_response(jsonify({"board": board_dict}), 201)


def check_duplicates(board_title):
    """
    check whether or not a board with a particular title already exists
    """
    test_board = Board.query.filter(Board.title == board_title).first()
    if test_board is not None:
        abort(
            make_response(
                {
                    "details": f"Board {board_title} already exists, please enter a unique title"
                },
                400,
            )
        )


@bp.route("", methods=["GET"])
def read_all_boards():
    boards = Board.query.all()

    boards_response = [board.to_dict() for board in boards]

    return jsonify(boards_response), 200


@bp.route("<board_title>", methods=["GET"])
def read_one_board(board_title):
    try:
        test_board = Board.query.filter(Board.title == board_title).first()

        return make_response(jsonify({"board": test_board.to_dict(cards=True)}))
    except:
        abort(make_response({"details": f"Board {board_title} invalid"}, 400))
