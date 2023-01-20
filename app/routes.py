from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from .models.board import Board
from .models.card import Card


boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"error": f"{cls.__name__} {model_id} invalid"}, 400))
    model = cls.query.get(model_id)
    if not model:
        abort(make_response(
            {"error": f"{cls.__name__} {model_id} not found"}, 404))
    return model


@boards_bp.route("", methods=["GET"])
def get_all_boards():
    board_query = Board.query
    boards = board_query.all()
    boards_response = [board.create_dict() for board in boards]
    return jsonify(boards_response), 200


@boards_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_model(Board, board_id)
    return {"board": board.create_dict()}, 200


@boards_bp.route("<board_id>/cards", methods=["GET"])
def get_cards_from_board(board_id):
    board = validate_model(Board, board_id)

    board_dict = board.create_dict()
    board_dict["cards"] = [card.create_dict() for card in board.cards]
    return board_dict, 200


@boards_bp.route("", methods=["POST"])
def create_board():
    try:
        request_body = request.get_json(force=True)
    except:
        return {"error": "Please include a request body with a title and owner"}, 400
    if not "title" in request_body or not "owner" in request_body:
        return {"error": "Please provide both the title and owner"}, 400
    new_board = Board(title=request_body["title"], owner=request_body["owner"])
    db.session.add(new_board)
    db.session.commit()

    return {
        "message": f"Board '{new_board.title}' successfully created",
        "board": new_board.create_dict()
    }, 201


@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_model(Board, board_id)
    cards = Card.query.filter_by(board_id=board_id)
    for card in cards:
        db.session.delete(card)
    db.session.delete(board)
    db.session.commit()
    return {"message": f"Board '{board.title}' successfully deleted"}, 200


@cards_bp.route("", methods=["GET"])
def get_all_cards():
    board_query = request.args.get("board_id")
    if board_query:
        cards = Card.query.filter_by(board_id=board_query)
    else:
        cards = Card.query.all()
    cards_response = [card.create_dict() for card in cards]
    return jsonify(cards_response), 200


@cards_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    card = validate_model(Card, card_id)
    return {"card": card.create_dict()}, 200


@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card, card_id)
    db.session.delete(card)
    db.session.commit()
    return {"message": f"Card {card_id} successfully deleted"}, 200


@cards_bp.route("/<card_id>", methods=["PUT"])
def update_likes_count(card_id):
    card = validate_model(Card, card_id)
    try:
        request_body = request.get_json(force=True)
    except:
        return {
            "error": "Please include a request body with a likes_count"
        }, 400
    if not "likes_count" in request_body:
        return {
            "error": "Please include a request body with a likes_count"
        }, 400
    else:
        card.likes_count = request_body["likes_count"]
    db.session.commit()
    return {
        "card": card.create_dict(),
        "message": "Likes count successfully updated"
    }, 200


@cards_bp.route("", methods=["POST"])
def create_card():
    try:
        request_body = request.get_json(force=True)
    except:
        return {"error": "Please include a request body with a message and board id"}, 400
    if not "message" in request_body or not "board_id" in request_body:
        return {"error": "Please provide a message and board id"}, 400
    requested_board_id = validate_model(Board, request_body["board_id"])
    new_card = Card(
        likes_count=0, message=request_body["message"], board_id=request_body["board_id"])
    db.session.add(new_card)
    db.session.commit()
    return {
        "message": f"Card '{new_card.message}' successfully created",
        "Card": new_card.create_dict()
    }, 201
