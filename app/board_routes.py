from  app import db
from app.models.board import Board
from flask import Blueprint, request, jsonify, make_response

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


@boards_bp.route("",  methods=["GET"])
def get_all_boards():
    all_boards = Board.query.all()
    board_titles = [[board.title, board.board_id] for board in all_boards]
    return jsonify(board_titles), 200


@boards_bp.route("",  methods=["POST"])
def create_one_board():
    if not request.is_json:
        return {"msg": "Missing JSON request body"}, 400
    request_body = request.get_json()
    try:
        title = request_body["title"]
        owner = request_body["owner"]
    
    except KeyError:
        return {"details": "Invalid data"}, 400
    
    new_board = Board(title=title, owner=owner)

    db.session.add(new_board)
    db.session.commit()
    
    rsp = {"board": new_board.get_dict()}
    return jsonify(rsp), 201
    # return jsonify(request_body["title"]), 201
    
    
@boards_bp.route("/<id>", methods=["GET"])
def get_cards_from_board(id):
    board = Board.query.get(id)
    if board is None:
        return jsonify(""), 404
    cards = []
    
    for card in board.cards:
        cards.append({
            "id": card.card_id,
            "message": card.message,
            "likes_count": card.likes_count
            })
        
    board_info = {
        "title": board.title,
        "owner": board.owner,
        "cards": cards,
        "id": int(id)
    }
    return jsonify(board_info), 200


@boards_bp.route("/<id>", methods=["DELETE"])
def delete_board(id):
    board = Board.query.get(id)
    if board is None:
        return jsonify(""), 404

    db.session.delete(board)
    db.session.commit()

    rsp = {"details": f'Board {id} "{board.title}" successfully deleted'}
    return jsonify(rsp), 200
