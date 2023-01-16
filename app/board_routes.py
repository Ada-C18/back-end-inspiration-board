from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

board_bp = Blueprint("board", __name__, url_prefix="/boards")


def get_validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


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

    return make_response(jsonify({"board": board.to_dict()}), 200)


# Delete Board
@board_bp.route("/<board_id>", strict_slashes=False, methods=["DELETE"])
def delete_board(board_id):
    board = get_validate_model(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    response_body = {
        "message": f'Board #{board_id} was deleted.'}
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
        print(request_body)
        new_board = Board.from_dict(request_body)
        print(new_board)

    except:
        return make_response({"message": "Invalid data"}, 400)

    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify(new_board.to_dict()), 201)


# Read ALL cards
@board_bp.route("/<board_id>/cards", strict_slashes=False, methods=["GET"])
def read_all_cards(board_id):
    board = get_validate_model(Board, board_id)
    # cards = Card.query.all()
    cards_list = [card.to_dict() for card in board.cards]
    # return make_response(jsonify(cards_list), 200)

    return make_response(jsonify({
            "board_id": board.board_id,
            "name": board.name,
            "owner": board.owner,
            "cards": cards_list
        }), 200)


# # Read one card
# @board_bp.route("/<board_id>/cards/<card_id>", strict_slashes=False, methods=["GET"])
# def read_one_card(board_id, card_id):
#     card = get_validate_model(Card, card_id)
#     board = get_validate_model(Board, board_id)

#     return make_response(jsonify(card.to_dict()), 200)     # board_id


# Create card
@board_bp.route("/<board_id>/cards/", strict_slashes=False, methods=["POST"])
def create_card(board_id):
    board = get_validate_model(Board, board_id)
    request_body = request.get_json()

    # board.cards = [Card.query.get(card_id) for card_id in request_body["card_ids"]]
    new_card = Card(message=request_body["message"])

    db.session.add(new_card)
    db.session.commit()
    return make_response(jsonify({
        "board_id": board_id,
        "card_id": new_card.card_id,
        "message": new_card.message,
        "likes": new_card.likes
    }), 200)
    return make_response(jsonify(dict(board_id=board.board_id, card_ids=[card.id for card in board.cards])), 200)   # 201
