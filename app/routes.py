from flask import Blueprint, request, jsonify, make_response,abort
from app.models.board import Board
from app.models.card import Card
from app import db

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint('board_bp', __name__, url_prefix='/board')

"""Board Routes"""
@board_bp.route("", methods=['POST'])
def add_one_board():
    response_body = request.get_json()
    try:
        new_board = Board.create_board(response_body)
    except KeyError:
        return make_response(jsonify({'warning':'invalid title or owner'}),400)
    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify({'msg':f'Board with id {new_board.board_id} created'}),201)

@board_bp.route("", methods=['GET'])
def get_all_boards():
    boards=Board.query.all()
    return_list=[]
    for board in boards:
        return_list.append(board.dictionfy())
    return make_response(jsonify(return_list),200)

@board_bp.route('/<board_id>', methods=['GET'])
def get_one_board_with_cards(board_id):
    board = validate_id(Board,board_id)
    board_info = board.dictionfy()
    return make_response(jsonify(board_info),200)

"""Card Routes"""

@board_bp.route('/<board_id>', methods=['POST'])
def add_one_card(board_id):
    request_body=request.get_json()
    try:
        new_card=Card.create_card(board_id,request_body)
    except KeyError:
        return make_response(jsonify({'warning':'invalid message'}),400)
    db.session.add(new_card)
    db.session.commit()

    return make_response(jsonify({'msg':f'Card with id {new_card.card_id} created'}),201)

@board_bp.route('/<board_id>/<card_id>', methods=['DELETE'])
def delete_one_card(board_id, card_id):
    card=validate_id(Card, card_id)
    db.session.delete(card)
    db.session.commit()

    return make_response(jsonify({'msg':f"card {card_id} deleted from Board with id {board_id}"}),200)








def validate_id(cls,id):
    try:
        model_id = int(id)
    except TypeError:
        abort(make_response({'details':'Invalid, id must be integer'}),400)
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({'details':'ID is invalid'}),404)
    return model