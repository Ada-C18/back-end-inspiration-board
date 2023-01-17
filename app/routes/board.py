from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

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


@bp.route("<board_id>/cards", methods=["GET"])
def read_all_cards(board_id):
    sort_query = request.args.get("sort")
    card_query = Card.query.filter(Card.board_id == board_id)
    if sort_query == "asc":
        card_query = card_query.order_by(Card.message.asc())
    elif sort_query == "likes":
        card_query = card_query.order_by(Card.likes_count.desc())
    else:
        card_query = card_query.order_by(Card.card_id)
    card_response = [card.to_dict() for card in card_query]

    return jsonify(card_response), 200
