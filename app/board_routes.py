from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint('board_bp', __name__, url_prefix='/board')

# get all boards
# create a board
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
        return make_response(jsonify(boards_response), 200)

    elif request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return {
                "Invalid data. Must include title"
            }, 400
        if "owner" not in request_body:
            return {
                "Invalid data. Must include owner"
            }, 400

        new_board = Board(
            title=request_body["title"], 
            owner=request_body["owner"]
        )

        db.session.add(new_board)
        db.session.commit()
    
        return make_response(f"Board {new_board.title} successfully created", 201)

# Get a board by ID
# Delete a board by ID
# Patch a board by ID
@board_bp.route("/<board_id>", methods=["GET", "PUT", "DELETE"])
def handle_board(board_id):
    board = Board.query.get(board_id)
    if board is None:
        return make_response(f"Board {board_id} not found.", 404)

    if request.method == "GET":
        # cards = []
        # for card in board.cards:
        #     single_card = {
        #         "message": card.message,
        #     }
        #     cards.append(single_card)
        # return make_response({
        #     "id": board.board_id,
        #     "title": board.title,
        #     "owner": board.owner,
        #     "cards": cards
        # })
        board = Board.query.get(board_id)

        return {"board": board.to_dict()}

    elif request.method == "PUT":
        form_data = request.get_json()
        board.title = form_data["title"]
        board.owner = form_data["owner"]

        db.session.commit()

        return make_response(f"Board: {board.title} sucessfully updated.")
    
    elif request.method == "DELETE":
        db.session.delete(board)
        db.session.commit()
        return make_response(f"Board: {board.title} sucessfully deleted.")