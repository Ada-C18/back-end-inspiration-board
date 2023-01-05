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

#Get Routes
@board_bp.route("", methods = ['GET'])
def get_all_boards():

    boards = Board.query.all()

    all_boards = [board.to_dict() for board in boards]

    return jsonify(all_boards)

@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_model(Board, board_id)
    return {"board": board.to_dict()}, 200


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

    except:
        abort(make_response({"details": "Invalid data"}, 400 ))

    db.session.add(new_card)
    db.session.commit()
    card_dict = new_card.to_dict()
    card_dict["board_id"] = new_card.board_id
    return {"message": new_card.message, "board_id": new_card.board_id}, 201



