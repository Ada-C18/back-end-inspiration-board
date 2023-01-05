from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint('board_bp', __name__, url_prefix='/board')

@board_bp.route("", methods=["GET", "POST"])
def handle_boards():
    if request.method == "GET":
        boards = Board.query.all()
        boards_response = []
        for board in boards:
            boards_response.append({
                "board_id": board.board_id,
                "title": board.title,
                "owner": board.owner,
            })
        return jsonify(boards_response)
    elif request.method == "POST":
        request_body = request.get_json()
        title = request_body.get("title")
        owner = request_body.get("owner")
        new_board = Board(title=request_body["title"], 
                        owner=request_body["owner"])

        db.session.add(new_board)
        db.session.commit()
    
    return make_response(f"Board {new_board.title} successfully created", 201)