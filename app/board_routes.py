from flask import Blueprint, request, jsonify, make_response, abort
# import requests
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)

board_bp = Blueprint('boards', __name__, url_prefix="/boards")

def validate_model(cls, model_id):
    try:
        model_id=int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__}{model_id} invalid"}, 400))
    model =  cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))
    return model
def add_cards_to_board(board):
    cards = board.cards
    all_cards = []
    for card in cards:
        all_cards.append({
            "message": card.message,
            "likes_count": card.likes_count,
            "card_id": card.card_id,
            "board_id": card.board_id,
        })
    board_dict = board.to_dict()
    board_dict["cards"] = all_cards
    return board_dict

#Get Routes
@board_bp.route("", methods = ['GET'])
def get_all_boards():

    boards = Board.query.all()

    all_boards = [add_cards_to_board(board) for board in boards]

    return jsonify(all_boards)

@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_model(Board, board_id)
    return {"board": add_cards_to_board(board)}, 200


@board_bp.route("", methods=["POST"])

def create_board():
    try:
        request_body = request.get_json()

        new_board = Board.from_dict(request_body)

    except:
        abort(make_response({"details": "Invalid data"}, 400 ))

    db.session.add(new_board)
    db.session.commit()

    return {"board": new_board.to_dict()}, 201

@board_bp.route("<board_id>", methods=["DELETE"])

def delete_board(board_id):
    board = validate_model(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    return make_response(jsonify({"details": f'Board {board.board_id} "{board.title}" successfully deleted'}),200)

# /Board/id/cards routes

@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_cards_for_specific_board(board_id):
    try:
        board = validate_model(Board, board_id)
        request_body = request.get_json()

        new_card = Card.from_dict(request_body)
        new_card.board_id = board_id
        db.session.add(new_card)
        db.session.commit()

    except:
        abort(make_response({"details": "Invalid data"}, 400 ))


    card_dict = new_card.to_dict()
    card_dict["board_id"] = new_card.board_id
    return {"message": new_card.message, "board_id": new_card.board_id}, 201

@board_bp.route("/<board_id>/cards", methods=["GET"])
def get_all_cards_for_specific_board(board_id):

    board = validate_model(Board, board_id)
    return add_cards_to_board(board)





