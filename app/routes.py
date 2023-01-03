from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    print(request_body)
    new_board = Board.from_dict(request_body)

    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify(f"Board {new_board.title} successfully created"), 201)

@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_card(board_id):

    board = validate_model(Board, board_id)

    request_body = request.get_json()
    new_card = Card(
        message=request_body["message"],
        likes=request_body["likes"],
        board=board
    )
    db.session.add(new_card)
    db.session.commit()
    return make_response(jsonify(f"Card {new_card.id} in {new_card.board.title} successfully created"), 201)

@boards_bp.route("/<board_id>/cards", methods=["GET"])
def retrieve_cards(board_id):

    board = validate_model(Board, board_id)

    cards_response = []
    for card in board.cards:
        cards_response.append(
            {
            "id": card.id,
            "message": card.message,
            "likes": card.likes
            }
        )
    return jsonify(cards_response)

