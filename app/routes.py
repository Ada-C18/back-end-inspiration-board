from os import abort
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# helper function
def validate_model(cls, model_id):
    try: 
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400)) 

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404)) 

    return model

#create a post route 
@boards_bp.route("", methods = ["POST"])
def create_board():
    request_body = request.get_json()

    try:
        new_board = Board.from_json(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_board)
    db.session.commit()

    return make_response(new_board.to_dict_boards(), 201)

#create a get route 
@boards_bp.route("", methods = ["GET"])
def get_one_board(board_id):
    board = validate_model(Board, board_id)

    return jsonify(board.to_dict_board()), 200






#create a route to delete a card



#create a route to delete all boards and cards 



# response bodies must have title, owner, and board_id 

