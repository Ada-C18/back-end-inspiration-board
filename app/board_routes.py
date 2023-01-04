from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
#======================================
#        CREATE ONE BOARD        
#====================================== 
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body or \
    "description" not in request_body:
        return make_response("Invalid Request", 400)
    
    new_board = Board.from_dict(request_body)
    
    db.session.add(new_board)
    db.session.commit()

    return jsonify({"board": new_board.to_dict()}), 201