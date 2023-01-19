from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.card import Card
from app.models.board import Board


def get_one_obj_or_abort(cls, obj_id):
    try:
        obj_id = int(obj_id)
    except ValueError:
        abort(make_response({"message":f"Invalid {cls.__name__} ID: `{obj_id}`. ID must be an integer"}, 400))

    matching_obj = cls.query.get(obj_id)

    if not matching_obj:
        abort(make_response({"message":f"{cls.__name__} with id `{obj_id}` was not found in the database."}, 404))

    return matching_obj


# **************************** CRUD ROUTES FOR BOARDS *****************************************

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["POST"])
def add_board():
    request_body = request.get_json()

    new_board = Board.from_json(request_body)

    db.session.add(new_board)
    db.session.commit()

    return {"board": new_board.to_json()}, 201


@boards_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()

    boards_response = [board.to_json() for board in boards]

    return jsonify(boards_response)


@boards_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    chosen_board = get_one_obj_or_abort(Board, board_id)

    board_json = chosen_board.to_json()

    return jsonify(board_json), 200

# ***************************** NESTED ROUTES FOR BOARDS AND CARDS *********************************

@boards_bp.route("/<board_id>/cards", methods=["POST"])
def add_board_card(board_id):
    chosen_board = get_one_obj_or_abort(Board, board_id)
    request_body = request.get_json()
    new_card = Card.from_json(request_body)

    new_card.board_id = chosen_board.board_id

    db.session.add(new_card)
    db.session.commit()

    return {"card": new_card.to_json()}, 201


@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_board_cards(board_id):
    chosen_board = get_one_obj_or_abort(Board, board_id)

    cards_response = [card.to_json() for card in chosen_board.cards]

    return jsonify({"chosen board id": chosen_board.board_id, "title": chosen_board.title, "chosen board cards": cards_response})


@boards_bp.route("/<board_id>/cards/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    chosen_card = get_one_obj_or_abort(Card, card_id)

    db.session.delete(chosen_card)

    db.session.commit()

    return jsonify({"message": f"Successfully deleted card with id `{card_id}`"}), 200


@boards_bp.route("/cards/<card_id>", methods=["GET"])
def get_one_card(card_id):
    chosen_card = get_one_obj_or_abort(Card, card_id)

    card_json = chosen_card.to_json()

    return jsonify(card_json), 200