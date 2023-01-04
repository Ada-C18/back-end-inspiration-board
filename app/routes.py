from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card


# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

def get_one_object_or_abort(cls, object_id):
    try:
        object_id = int(object_id)
    except ValueError:
        response_str = f"Invalid ID: {object_id}"
        abort(make_response(jsonify({
            "message": response_str
            }), 400))

    matching_object = cls.query.get(object_id)

    if not matching_object:
        response_str = f"{object_id} not found"
        abort(make_response(jsonify({
            "message": response_str
            }), 404))
    
    return matching_object

#Endpoints
#GET - /boards
@boards_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()

    boards_response = []
    for board in boards:
        boards_response.append(
            {
                "title": board.title,
                "owner": board.owner
            }
        )
    return jsonify(boards_response)

#POST -/boards
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    new_board = Board(title=request_body["title"],
    owner = request_body["owner"])

    db.session.add(new_board)
    db.session.commit()

    return make_response(f"{new_board.title} created", 201)

#GET - /boards/<board_id>/cards




#POST - /boards/<board_id>/cards
#DELETE - /cards/<card_id>
#PUT - /cards/<card_id>/like