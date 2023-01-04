from flask import abort, Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("board", __name__,url_prefix="/boards")
card_bp = Blueprint("card", __name__,url_prefix="/cards")

#GET route for ALL boards
@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    result = []
    for board in boards:
        result.append(board.to_dict())
        # need to create to_dict method in Board Model
    return jsonify(result), 200

#GET route for ONE board
def get_board_from_id(board_id):
    chosen_board = Board.query.get(board_id)
    if chosen_board is None:
        return abort(make_response({"msg": f"Could not find board with id: {board_id}"}, 404))
    return chosen_board


#POST route for ONE board
@board_bp.route("",methods=["POST"])
def create_one_board():
    request_body = request.get_json()
    try:
        new_board = Board(
            title=request_body["title"],
            owner=request_body["owner"]            
        )
    except:
        return abort(make_response({"details": "Invalid data"}, 400))
    db.session.add(new_board)
    db.session.commit()
    return jsonify({"board":new_board.to_dict()}),201

#POST route for ONE card
@card_bp.route("/<board_id>", methods=["POST"])
def create_one_card():
    request_body = request.get_json()
    try:
        new_card = Card(
            message=request_body["message"]
        )
    except:
        return abort(make_response({"details": "Invalid data"}, 400))
    db.session.add(new_card)
    db.session.commit()
    return jsonify({"card":new_card.to_dict()}),201

#Get route for ALL cards
@card_bp.route("/<board_id>", methods=["GET"])
def get_all_cards(board_id):
    board = get_board_from_id(board_id)
    cards = Card.query.all()
    result = []
    for card in cards:
        result.append(card.to_dict())
    # lines 63-65 will be a seperate function in Board model
    # function: get_cards_list()
    # need to create a to_dict_relationship in Board model
    # id, title, owner, cards: self.get_cards_list()
    # result = board.to_dict_relationship
    return jsonify(result), 200