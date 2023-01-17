from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from .models.board import Board
from .models.card import Card
from app.card_routes import validate_cards
from sqlalchemy import asc,desc

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


@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body or "owner" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_board = Board(
        title=request_body["title"],
        owner=request_body["owner"])
    db.session.add(new_board)
    db.session.commit()
    return jsonify(new_board.to_dict()), 201

# Get all board

# @boards_bp.route("", methods=["GET"])
# def get_all_board():
#     board_param = request.args
#     boards = Board.query.all()
#     boards_response = []
#     for board in boards:
#         boards_response.append({
#             "id": board.board_id,
#             "title": board.title,
#             "owner": board.owner
#         })
#     return jsonify(boards_response), 200
@boards_bp.route("", methods =["GET"])
def get_all_board():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        boards =Board.query.order_by(asc(Board.title))
    elif sort_query == "desc":
        boards = Board.query.order_by(desc(Board.title))
    else:
        boards = Board.query.all()
    return jsonify([board.to_dict_board() for board in boards]), 200


# update board by id
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_one_card(board_id):
    # board = validate_cards(card_id)
    request_body = request.get_json()
    if 'message' not in request_body:
        return {"message": "Please enter both message and likes"}, 400

    new_card = Card(message=request_body['message'],
                    board_id=int(board_id)
                    )
    # for card_id in request_body["card_ids"]:
    #     card = validate_cards(card_id)
    #     card.board = board
    #     card_list.append(card_id)

    db.session.add(new_card)
    db.session.commit()

    return jsonify({
        "id": new_card.card_id,
        "message": new_card.message,
        "likes_count": new_card.likes_count,
        "board_id": new_board.id
    }), 201

# helper function

def get_board_or_abort(board_id):
    try:
        board_id = int(board_id)
    except ValueError:
        abort(make_response(
            {"message": f"The board id {board_id} is invalid. The id must be integer."}, 400))
    boards = Board.query.all()
    for board in boards:
        if board.board_id == board_id:
            return board
    abort(make_response(
        {"message": f"The board id {board_id} is not found"}, 404))


@boards_bp.route('/<board_id>', methods=["GET"])
def get_one_board(board_id):
    board = get_board_or_abort(board_id)
    return jsonify({"board": board.to_dict_board()}), 200


@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_of_board(board_id):
    board = validate_board(board_id)
    card_dict = [card.to_dict() for card in board.cards]
    result = board.to_dict()
    result["cards"] = card_dict

    return jsonify(result), 200

@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_by_board(board_id):
    chosen_board = get_board_or_abort(board_id)
    response_body = [card.to_dict() for card in chosen_board.cards]
    return jsonify(response_body),200

@boards_bp.route("/<board_id>", methods=["Delete"])
def delete_board(board_id):
    chosen_board = get_board_or_abort(board_id)
    db.session.delete(chosen_board)
    db.session.commit()
    return jsonify(f"successfully deleted {chosen_board.title}"),200
