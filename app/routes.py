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
                "id": board.id,
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

    return new_board.to_dict(), 201

#GET - /boards/<board_id>/cards
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_all_cards_belonging_to_board_id(board_id):
    board = get_one_object_or_abort(Board, board_id)

    board_response = [card.to_dict() for card in board.cards]

    return jsonify(board_response), 200

#POST - /boards/<board_id>/cards
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def post_card_belonging_to_board(board_id):
    parent_board = get_one_object_or_abort(Board, board_id)

    request_body = request.get_json()
    new_card = Card.from_dict(request_body)
    new_card.board = parent_board

    db.session.add(new_card)
    db.session.commit()

    return new_card.to_dict(), 201

#DELETE - /cards/<card_id>
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    chosen_card = get_one_object_or_abort(Card, card_id)

    db.session.delete(chosen_card)
    db.session.commit()

    return jsonify({"Message": f"{card_id} successfully deleted."}), 200

#PATCH - /cards/<card_id>/like
@cards_bp.route("/<card_id>/<new_likes_count>", methods=["PATCH"])
def update_one_card_likes_count(card_id, new_likes_count):
    chosen_card = get_one_object_or_abort(Card, card_id)
    try:
        new_likes_count = int(new_likes_count)
    except ValueError:
        response_str = f"Invalid likes count: {new_likes_count} must be an integer."
        return jsonify({"Message": response_str}), 400
    
    chosen_card.likes_count = new_likes_count

    db.session.commit()
    return chosen_card.to_dict(), 200