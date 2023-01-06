from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(jsonify({"message":f"{cls.__name__} {model_id} not found"}), 404))
    
    return model

#### Board Routes #####

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

# GET /boards
@boards_bp.route("", methods=["GET"])
def read_all_boards():
    boards = Board.query.all()

    boards_response = []
    for board in boards:
        boards_response.append(board.to_dict())
    return jsonify(boards_response)


# POST /boards
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    try:
        new_board = Board.from_dict(request_body)
    except:
        abort(make_response({"details": "Missing data"}, 400))

    db.session.add(new_board)
    db.session.commit()

    return make_response(new_board.to_dict() #changed this from Board.to_dict()
        , 201)
# Create a new board, by filling out a form. The form includes "title" and "owner" name of the board.
# See an error message if I try to make a new board with an empty/blank/invalid/missing "title" or "owner" input.
# All error messages can look like a new section on the screen, a red outline around the input field, and/or disabling the input, as long as it's visible

@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_model(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    return make_response({"details":f'Board {board_id} "{board.title}" successfully deleted'})

# GET /boards/<board_id>/cards
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def read_cards_of_board(board_id):
    board = validate_model(Board, board_id)

    cards_response = []
    for card in board.cards:
        cards_response.append(card.to_dict()
        )
    return jsonify(cards_response)

# POST /boards/<board_id>/cards
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def add_one_card_to_board(board_id):
    validate_model(Board, board_id)

    request_body = request.get_json()
    new_card = Card(
        message=request_body["message"],
        likes_count=request_body["likes_count"],
        board_id=request_body["board_id"]
    )
    db.session.add(new_card)
    db.session.commit()
    return jsonify(new_card.to_dict()), 200 #changed this so that it returns the card as the response
# Create a new card for the selected board, by filling out a form and filling out a "message."
# See an error message if I try to make the card's "message" more than 40 characters.
# All error messages can look like a new section on the screen, a red outline around the input field, and/or disabling the input, as long as it's visible