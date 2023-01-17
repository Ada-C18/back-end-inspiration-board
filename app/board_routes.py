from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint('board_bp', __name__, url_prefix='/board')

# non-route functions
def validate_board(board_id):
    try:
        board_id = int(board_id)
    except:
        abort(make_response({"error message":f"Board {board_id} invalid"}, 400))

    board = Board.query.get(board_id)

    if not board:
        abort(make_response({"error message":f"Board {board_id} not found"}, 404))

def validate_card(card_id):
    # used to determine correct type for card search
    try:
        card_id = int(card_id)
    except:
        abort(make_response({"error message":f"{card_id} is an invalid input."}, 400))
    
    card = Card.query.get(card_id)

    # used to determine if searched card is within database
    if not card:
        abort(make_response({"error message":f"Card ID {card_id} not found."}, 404))
    
    return card

# get all boards
@board_bp.route("", methods=["GET"])
def get_boards():
    boards = Board.query.all()
    boards_response = []
    for board in boards:
        boards_response.append({
            "board_id": board.board_id,
            "title": board.title,
            "owner": board.owner,
        })
    return make_response(jsonify(boards_response), 200)


# create a board
@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({ "error message" :
            "Invalid data. Must include title"
        }, 400)
    if "owner" not in request_body:
        return make_response({"error message" :
            "Invalid data. Must include owner"
        }, 400)

    new_board = Board(
        title=request_body["title"], 
        owner=request_body["owner"]
    )

    db.session.add(new_board)
    db.session.commit()
    
    return make_response({"board":new_board.to_dict()}, 201)

# Get a board by ID
# Delete a board by ID
# Patch a board by ID
@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_board(board_id)
    board = Board.query.get(board_id)
    
    return {"board": board.to_dict()}

@board_bp.route("/<board_id>", methods=["PUT"])
def update_one_board(board_id):
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({"error message":
            "Invalid data. Must include title"
        }, 400)
    if "owner" not in request_body:
        return make_response({"error message":
            "Invalid data. Must include owner"
        }, 400)

    board = validate_board(board_id)
    board = Board.query.get(board_id)
    
    board.title = request_body["title"]
    board.ownder = request_body["owner"]

    db.session.commit()
    return make_response({"board":board.to_dict()}, 200)
    
@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_one_board(board_id):
    board = validate_board(board_id)
    board = Board.query.get(board_id)

    db.session.delete(board)
    db.session.commit()

    return make_response({"message": "Board successfully deleted"}, 200)

@board_bp.route("/<board_id>/cards", methods=["POST"])
def add_card_to_board(board_id):
    board = validate_board(board_id)
    board = Board.query.get(board_id)

    request_body = request.get_json()

    # ensures minimum input for card; its message
    if "message" not in request_body:
        return make_response({"error message": "Invalid input"}, 400)

    # managing the character limit
    if len(request_body["message"]) < 1:
        return make_response({"error message": "Input cannot be empty."}, 400)
    if len(request_body["message"]) > 40:
        return make_response({"error message": "Input exceeds character limit."}, 400)

    # id and likes count should be automatically added
    new_card = Card(
        message = request_body["message"])

    new_card.board_id = board.board_id

    db.session.add(new_card)
    db.session.commit()

    return make_response(new_card.to_dict(), 200)

@board_bp.route("/<board_id>/cards", methods=["GET"])
def get_all_cards_per_board(board_id):
    board = validate_board(board_id)
    board = Board.query.get(board_id)

    return_body = board.to_dict()
    return_body["cards"] = [card.to_dict() for card in board.cards]

    return make_response(jsonify(return_body), 200)

@board_bp.route("/<board_id>/cards/<card_id>", methods=["DELETE"])
def delete_card_from_board(board_id, card_id):
    board = validate_board(board_id)

    card = validate_card(card_id)
    card = Card.query.get(card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response({"message": "Card successfully deleted"}, 200)

