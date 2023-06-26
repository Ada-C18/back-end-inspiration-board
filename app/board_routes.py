from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("boards", __name__, url_prefix="/boards")

#Create board (POST)
@board_bp.route("", methods=["POST"])
def create_new_board():
    request_body = request.get_json()

    new_board = Board(title=request_body["title"],
                    owner=request_body["owner"])

    db.session.add(new_board)
    db.session.commit()

    return make_response(f"Board {new_board.title} successfully created", 201)

#Read board (GET)

#Read all boards? (GET)



#Delete board (DELETE)
