from flask import Blueprint, request, jsonify, make_response
from .card_routes import validate_model
from app.models.card import Card
from app.models.board import Board
from app import db

board_bp = Blueprint('board_bp', __name__, url_prefix='/boards')


@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    title = request_body['title']
    owner = request_body['owner']
    if len(request_body) != 2:
        return {"details": "Invalid Data"}, 400

    if not owner or not title:
        return {"details": "Title and/or Owner was left blank"}
    new_board = Board.from_dict_to_object(request_body)

    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify({"board": new_board.to_dict()}), 201)


@board_bp.route("/<id>", methods=["GET"])
def read_specific_board(id):
    board = validate_model(Board, id)
    response_body = board.to_dict()
    return make_response(jsonify(response_body), 200)


@board_bp.route("", methods=["GET"])
def read_all_boards():
    boards = Board.query.all()
    board_response = [board.to_dict() for board in boards]

    return make_response(jsonify(board_response), 200)


@board_bp.route("/<board_id>/cards", methods=["GET"])
def read_all_cards(board_id):
    board = validate_model(Board, board_id)
    boards_response = [card.to_dict() for card in board.cards]
    return(jsonify(boards_response))


@board_bp.route("/<board_id>/cards", methods=["POST"])
def add_card_to_board(board_id):
    request_body = request.get_json()
    message = request_body["message"]
    if not message:
        return {"details": "Invalid Data"}, 400
    if len(message) > 40:
        return {"details": "You have gone over the 40 character message limit."}
    new_card = Card.from_dict_to_object(request_body)

    db.session.add(new_card)


    board = validate_model(Board, board_id)
    board.cards.append(new_card)

    db.session.commit()

    return make_response(jsonify({'board_id': board.board_id, 'cards': [card.to_dict() for card in board.cards]}), 200)


@board_bp.route("/<id>", methods=["DELETE"])
def delete_board(id):
    board = validate_model(Board, id)

    db.session.delete(board)
    db.session.commit()

    return make_response(jsonify({"details": f"Board {id} '{board.title}' successfully deleted"}), 200)
