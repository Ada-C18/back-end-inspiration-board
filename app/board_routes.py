from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from datetime import datetime


bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

@bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    
    if request_body["title"] is None:
        abort(make_response({"message":"Please include a title"}, 400))
    
    # if request_body["owner"] is None:
    #     abort(make_response({"message":"Please include an owner"}, 400))
    # Since we have a login, they can't encounter this error in the first place
    
    date = str(datetime.utcnow())

    new_board = Board.from_dict({'date_created': date, 'title':request_body["title"], 
                                'owner_id':request_body['user_id'], 'card_color': request_body['card_color'], 'visible':True})

    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify(new_board.to_dict()), 201)

@bp.route("", methods=["GET"])
def read_all_boards():

    title_query = request.args.get("title")
    if title_query:
        boards = Board.query.filter_by(title=title_query)
    else:
        boards = Board.query.all()

    boards_response = []

    for board in boards:
        boards_response.append(board.to_dict())

    return jsonify(boards_response)

@bp.route("<board_id>", methods=["GET"])
def read_one_board(board_id):
    board = validate_model(Board, board_id)
    return board.to_dict()

@bp.route("<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_model(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    return make_response(jsonify(f"Board #{board.id} successfully deleted"))
