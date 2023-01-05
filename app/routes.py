from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.card import Card
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)

cards_bp = Blueprint("cards",__name__, url_prefix="/cards")

@cards_bp.route("", methods=["POST", "GET"])
def get_or_post_cards():
    if request.method=="GET":
        cards=Card.query.all()
        cards_response=[]
        for card in cards:
            cards_response.append({
                "id":card.id,
                "message":card.message
            })
        return jsonify(cards_response)
    
    elif request.method =="POST" :
        request_body=request.get_json()
        new_card = Card(message= request_body["message"])

        db.session.add(new_card)
        db.session.commit()

        return make_response(f"Card {new_card.message} successfully created", 201)

        


def validate_id(cls, id):
    try: 
        id = int(id)
    except:
        abort(make_response ({"message":f"{cls.__name__}{id} invalid"}, 400))

    obj = cls.query.get(id)

    if not obj:
        abort(make_response({"message":f"{cls.__name__} {id} not found"}, 404))

    return obj

@cards_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    card = validate_id(Card, card_id)

    return {
        "message": card.message
    }

#have a call to update board
@cards_bp.route("/<id>",methods=["DELETE"])
def delete_card(id):
    card=validate_id(Card,id)
    db.session.delete(card)
    db.session.commit()
    return make_response({"details":f'Card {id} " {card.message} "  successfully deleted'})

boards_bp = Blueprint("boards",__name__, url_prefix="/boards")


@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_boards(board_id):
    board = validate_id(Board, board_id)

    response_body = []
    for card in board.cards:
        response_body.append(card.card_dict())

    return {
        "id": board.id,
        "title": board.title,
        "author": board.author,
        "cards": response_body
    }

@boards_bp.route("", methods=["POST"])
def create_board():
    request_body=request.get_json()
    new_board = Board(title= request_body["title"],author=request_body["author"])

    db.session.add(new_board)
    db.session.commit()

    return make_response(f"Board {new_board.title} successfully created", 201)


@boards_bp.route("<board_id>/cards", methods=["POST"])
def create_card(id):
    board_query = Board.query.get(id)

    request_body = request.get_json()
    new_card = Card(
        message=request_body["message"],
        board = board_query
    ) 

    db.session.add(new_card)
    db.session.commit()

    return make_response(f"Card {new_card.message} has been created", 201)


@boards_bp.route("", methods=["GET"])
def get_all_board():
    board_list = []

    boards= Board.query.all()

    for board in boards:
        board_list.append(board.board_dict())
    
    return jsonify(board_list)
