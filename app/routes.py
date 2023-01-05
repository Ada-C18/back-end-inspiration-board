from flask import abort, Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("board", __name__,url_prefix="/boards")
card_bp = Blueprint("card", __name__,url_prefix="/cards")

# Helper Functions
def get_board_from_id(board_id):
    chosen_board = Board.query.get(board_id)
    if chosen_board is None:
        return abort(make_response({"msg": f"Could not find board with id: {board_id}"}, 404))
    return chosen_board

def get_card_from_id(card_id):
    chosen_card = Card.query.get(card_id)
    if chosen_card is None:
        return abort(make_response({"msg": f"Could not find board with id: {card_id}"}, 404))
    return chosen_card

#GET route for ALL boards
@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    result = []
    for board in boards:
        result.append(board.to_dict())
        # need to create to_dict method in Board Model
    return jsonify(result), 200

#POST route for ONE board
@board_bp.route("",methods=["POST"])
def create_one_board():
    request_body = request.get_json()
    try:
        new_board = Board(
            title=request_body["title"],
            owner=request_body["owner"]            
        )
    except:
        return abort(make_response({"details": "Invalid data"}, 400))

    
    db.session.add(new_board)
    db.session.commit()
    return jsonify({"board":new_board.to_dict()}),201

#POST route for ONE card for specific board
@card_bp.route("/<board_id>", methods=["POST"])
def create_one_card(board_id):
    board = get_board_from_id(board_id)
    request_body = request.get_json()
    try:
        new_card = Card(
            message=request_body["message"]
        )
    except:
        return abort(make_response({"details": "Invalid data"}, 400))
    
    new_card.board_id = board.board_id
    
    db.session.add(new_card)
    db.session.commit()
    return jsonify({"card":new_card.to_dict()}),201

#Get route for ONE Board and ALL its cards
@board_bp.route("/<board_id>", methods=["GET"])
def get_all_cards(board_id):
    board = get_board_from_id(board_id)
    
    result = board.to_dict_relationship()
    
    return jsonify(result), 200

#Get route for ONE CARD
#Should endpoint be named differently. Line 45 vs Line 74
@card_bp.route("", methods=["GET"])
def get_all_cards():
    cards = Card.query.all()
    result = []
    for card in cards:
        result.append(card.to_dict())
        # need to create to_dict method in Board Model
    return jsonify(result), 200

@card_bp.route("/<card_id>",methods=["GET"])
def get_one_card(card_id):
    chosen_card = Card.query.get(card_id)
    if chosen_card is None:
        return abort(make_response({"msg": f"Could not find card with id: {card_id}"}, 404))
    return jsonify({"card":chosen_card.to_dict()}), 200
   
#DELETE route for one board
@board_bp.route("/<board_id>",methods=["DELETE"])
def delete_board(board_id):
    board = get_board_from_id(board_id)
    board_title = board.title
    
    db.session.delete(board)
    db.session.commit()
    return jsonify({"Details": f'board {board_id} "{board_title}" successfully deleted.'}), 200

#DELETE route for one card
@card_bp.route("/<card_id>",methods=["DELETE"])
def delete_card(card_id):
    chosen_card = get_card_from_id(card_id)
    db.session.delete(chosen_card)
    db.session.commit()
    return jsonify({"Details": f'card {card_id} successfully deleted.'}), 200

#PATCH route to increase likes_count
@card_bp.route("/<card_id>/<updated_likes_count>", methods=["PATCH"])
def update_one_card_like_count(card_id,updated_likes_count):
    card = get_card_from_id(card_id)
    
    try:
        updated_likes_count = int(updated_likes_count)
    except:
        response_str = f"Invalid like counts: `{updated_likes_count}`. New price must be an integer"
        return jsonify({"message":response_str}), 400
    
    card.likes_count = updated_likes_count
    
    db.session.commit()
    
    return jsonify({"message": f"Successfully updated Card ID `{card_id}`'s price to be {updated_likes_count}"}), 200
        
