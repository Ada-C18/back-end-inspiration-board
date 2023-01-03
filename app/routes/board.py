from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.routes.routes_helper import validate_model, validate_input_data, error_message
from app.models.board import Board

boards_bp = Blueprint('boards_bp', __name__, url_prefix = '/boards')

# read one board (GET)
@boards_bp.route("/<id>", methods=["GET"])
def read_one_board(id):
    board = validate_model(Board, id)

    return jsonify({"board": board.to_dict()}), 200
     
    
    
# read all boards (GET)
@boards_bp.route("", methods=["GET"])
def read_all_boards():

    boards = Board.query.all()

    boards_response = [board.to_dict() for board in boards]
    return jsonify(boards_response)


# create a board (POST) 
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    new_board = validate_input_data(Board, request_body)

    db.session.add(new_board)
    db.session.commit()

    return jsonify({"board": new_board.to_dict()}), 201


# update a board (PUT)
@boards_bp.route("/<id>", methods=["PUT"])
def update_board(id):
    board = validate_model(board, id)
    request_body = request.get_json()

    board.update(request_body)
    db.session.commit()
    
    response = {"board": board.to_dict()}
    return response

# delete a board
@boards_bp.route("/<id>", methods=["DELETE"])
def delete_board(id):
    board = validate_model(board, id)
    title = str(board.title)
    db.session.delete(board)
    db.session.commit()

    return(make_response({"details": f"board {id} \"{title}\" successfully deleted"}), 200)

