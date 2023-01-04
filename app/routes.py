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

@boards_bp.route("", methods=["GET"])
def read_all_boards():
    
    boards = Board.query.all()

    boards_response = []
    for board in boards:
        boards_response.append(
            {
                "title": board.title,
                "owner_name": board.owner_name,
                "id": board.id
            }
        )
    return jsonify(boards_response)
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_card(board_id):

    board = validate_model(Board, board_id)

    request_body = request.get_json()
    new_card = Card(
        message=request_body["message"],
        likes=0,
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


#  delete route 

@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_model(Board,board_id)

    db.session.delete(board)
    db.session.commit()

    return make_response(jsonify(f"Board {board.title} with id #{board.id} successfully deleted"))


@boards_bp.route("/<board_id>/cards/<card_id>", methods=["DELETE"])
def delete_card(board_id, card_id):

    board = validate_model(Board, board_id)

    cards_response = []
    for card in board.cards:
        if card.id == int(card_id):
            db.session.delete(card)
        else:
            cards_response.append(
                {
                "id": card.id,
                "message": card.message,
                "likes": card.likes
                }
            )
    db.session.commit()
    return jsonify(cards_response)

@boards_bp.route("/<board_id>/cards/<card_id>", methods=["PATCH"])
def update_likes(board_id, card_id):

    board = validate_model(Board, board_id)

    card_response = {}
    for card in board.cards:
        if card.id == int(card_id):
            card.likes += 1
            card_response =  {
                "id": card.id,
                "message": card.message,
                "likes": card.likes
                }
    db.session.commit()
    return jsonify(card_response)