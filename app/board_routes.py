from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
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
        return make_response("Invalid Request", 400)
    
    new_board = Board.from_dict(request_body)
    
    db.session.add(new_board)
    db.session.commit()

    return jsonify({"board": new_board.to_dict()}), 201



#===================================
#        READ ONE BOARD BY ID
#===================================

@boards_bp.route("/<board_id>", methods=["GET"])
def read_one_board(board_id):
    board = validate_model(Board, board_id)
    response_one_board = {"board": Board.to_dict(board)}
    return jsonify(response_one_board), 200

