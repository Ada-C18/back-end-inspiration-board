from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    print(request_body)
    new_board = Board.from_dict(request_body)

    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify(f"Board {new_board.title} successfully created"), 201)

@boards_bp.route("", methods=["GET"])
def read_all_boards():
    
    boards = Board.query.all()

    boards_response = []
    for board in boards:
        boards_response.append(
            {
                "title": board.title,
                "owner_name": board.owner_name

            }
        )
    return jsonify(boards_response)
