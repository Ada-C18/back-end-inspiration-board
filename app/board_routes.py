from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
from app.validate_data import validate_model

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


#======================================
#        CREATE ONE BOARD        
#====================================== 

@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body or \
            "owner" not in request_body:
        return make_response({"details":"Invalid request; missing necessary field(s)"}, 400)

    new_board = Board.from_dict(request_body)

    db.session.add(new_board)
    db.session.commit()

    return jsonify({"board": new_board.to_dict()}), 201



#======================================
#        GET ALL BOARDS
#======================================


@boards_bp.route("", methods=["GET"])
def read_all_boards():

    boards = Board.query.all()

    boards_response = []  # returns empty list if no goals

    for board in boards:
        boards_response.append({
            "board_id": board.board_id,
            "title": board.title,
            "owner": board.owner,
        })

    return jsonify(boards_response), 200


# ===================================
#        READ ONE BOARD BY ID
# ===================================

@boards_bp.route("/<board_id>", methods=["GET"])
def read_one_board(board_id):
    board = validate_model(Board, board_id)
    response_one_board = {"board": Board.to_dict(board)}
    return jsonify(response_one_board), 200


#======================================
#        CREATE ONE CARD        
#====================================== 

@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_card(board_id):
    validate_board = validate_model(Board, board_id)
    board = Board.query.get(validate_board.board_id)

    request_body = request.get_json()

    if not "message" in request_body:
        return make_response({"details":"Invalid request; message field missing"}, 400)
    elif len(request_body["message"]) < 1:
        return make_response({"details":"Invalid request; message field cannot be empty"}, 400)
    elif len(request_body["message"]) > 40:
        return make_response({"details":"Invalid request; message over 40 characters"}, 400)

    new_card = Card.from_dict(request_body, board)

    db.session.add(new_card)
    db.session.commit()

    return {"card": new_card.to_dict()}, 201


#======================================
#        GET ALL CARDS FOR BOARD        
#====================================== 

@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_for_board(board_id):
    board = validate_model(Board, board_id)
    board_dict = board.to_dict(cards=True)
    sort_param = request.args.get("sort")

    if sort_param == "id":
        board_dict["cards"].sort(key=lambda c: c.get("id"))
    elif sort_param == "alphabet":
        board_dict["cards"].sort(key=lambda c: c.get("message"))
    elif sort_param == "likes":
        board_dict["cards"].sort(key=lambda c: c.get("likes_count"), reverse=True) #descending order starting from lagest number of likes

    return board_dict
