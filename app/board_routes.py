from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board

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
    pass

# POST /boards
@boards_bp.route("", methods=["POST"])
def create_board():
    pass
# Create a new board, by filling out a form. The form includes "title" and "owner" name of the board.
# See an error message if I try to make a new board with an empty/blank/invalid/missing "title" or "owner" input.
# All error messages can look like a new section on the screen, a red outline around the input field, and/or disabling the input, as long as it's visible

# GET /boards/<board_id>/cards
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def read_cards_of_board():
    pass

# POST /boards/<board_id>/cards
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def add_one_card_to_board():
    pass
# Create a new card for the selected board, by filling out a form and filling out a "message."
# See an error message if I try to make the card's "message" more than 40 characters.
# All error messages can look like a new section on the screen, a red outline around the input field, and/or disabling the input, as long as it's visible