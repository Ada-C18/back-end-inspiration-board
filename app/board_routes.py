from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
from app.helper_func import get_validate_model, send_message_to_slack

board_bp = Blueprint("board", __name__, url_prefix="/boards")


# Read ALL boards
@board_bp.route("", strict_slashes=False, methods=["GET"])
def read_all_boards():
    boards = Board.query.all()
    boards_list = [board.to_dict() for board in boards]
    return make_response(jsonify(boards_list), 200)


# Read ONE board
@board_bp.route("/<board_id>", strict_slashes=False, methods=["GET"])
def read_one_board(board_id):
    board = get_validate_model(Board, board_id)
    return make_response(jsonify(board.to_dict()), 200)


# Delete Board
@board_bp.route("/<board_id>", strict_slashes=False, methods=["DELETE"])
def delete_board(board_id):
    board = get_validate_model(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    response_body = {"message": f"Board #{board_id} was deleted."}
    return make_response(jsonify(response_body), 200)


# Update Board
@board_bp.route("/<board_id>", strict_slashes=False, methods=["PUT"])
def update_board(board_id):
    board = get_validate_model(Board, board_id)

    request_body = request.get_json()
    board.name = request_body["name"]
    board.owner = request_body["owner"]

    db.session.commit()

    current_board_response = board.to_dict()
    return make_response(jsonify(current_board_response), 200)


# Create Board
@board_bp.route("/", strict_slashes=False, methods=["POST"])
def create_board():
    try:
        request_body = request.get_json()
        new_board = Board.from_dict(request_body)

    except:
        return make_response(
            {"message": "Invalid data. Please check input for board."}, 400
        )

    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify(new_board.to_dict()), 201)


# Read ALL cards
@board_bp.route("/<board_id>/cards", strict_slashes=False, methods=["GET"])
def read_all_cards(board_id):
    board = get_validate_model(Board, board_id)

    cards_list = [card.to_dict() for card in board.cards]
    cards_list.sort(key=lambda c: c["card_id"])

    return make_response(
        jsonify(
            {
                "board_id": board.board_id,
                "name": board.name,
                "owner": board.owner,
                "cards": cards_list,
            }
        ),
        200,
    )


# Create card
@board_bp.route("/<board_id>/cards/", strict_slashes=False, methods=["POST"])
def create_card(board_id):
    try:
        board = get_validate_model(Board, board_id)
        request_body = request.get_json()
        new_card = Card(message=request_body["message"], board_id=board_id)
    except:
        return make_response(
            {"message": "Invalid data. Please check input for card."}, 400
        )

    db.session.add(new_card)
    db.session.commit()
    send_message_to_slack(new_card)
    return make_response(jsonify(new_card.to_dict()), 201)
