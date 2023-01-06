from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from .models.board import Board
from .models.card import Card
from app.card_routes import validate_cards

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint('boards_bp', __name__, url_prefix="/boards")

def validate_board(board_id):
    try:
        board_id = int(board_id)
    except:
        abort(make_response({"message": f"Board {board_id} invalid."}, 400))
    board = Board.query.get(board_id)
    if not board:
        abort(make_response({"message": f"Board {board_id} not found."}, 404))
        return board
# create a board
@boards_bp.route("", methods =["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body or "owner" not in request_body:
        return jsonify({"details":"Invalid data"}), 400
    
    new_board = Board (
        title=request_body["title"],
        owner=request_body["owner"])
    db.session.add(new_board)
    db.session.commit()
    return jsonify(new_board.to_dict()), 201

#Get all board
@boards_bp.route("", methods =["GET"])
def get_all_board():
    board_param = request.args
    boards = Board.query.all()
    boards_response = []
    for board in boards:
        boards_response.append({
            "id": board.board_id,
            "title": board.title,
            "owner": board.owner
        })
    return jsonify(boards_response), 200

#update board by id
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def update_board_cards(board_id):
    board = validate_board(board_id)
    request_body = request.get_json()
    card_list = []
    for card_id in request_body["card_ids"]:
        card = validate_cards(card_id)
        card.board = board
        card_list.append(card_id)
    db.session.commit()
    return jsonify({
        "id": board.board_id,
        "card_ids": card_list
    }), 201

@boards_bp.route('/<board_id>', methods= ["GET"])
def get_one_board(board_id):
    board = validate_board(board_id)
    return jsonify(board.to_dict()), 200


@boards_bp.route("/<board_id>/cards", methods =["GET"])
def get_cards_of_board(board_id):
    board = validate_board(board_id)
    card_dict = [card.to_dict() for card in board.cards]
    result = board.to_dict()
    result["cards"] = card_dict

    return jsonify(result), 200
