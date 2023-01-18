from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from datetime import datetime
from app.board_routes import validate_model
from app.models.board import Board


bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

# Create a card [POST]
@bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()

    if not request_body["user_id"]:
        abort(make_response({"message": "No user ID present"}, 400))

    if not request_body["message"]:
        abort(make_response({"message": "No message in card"}, 400))

    date = str(datetime.utcnow())

    new_card = Card.from_dict({'date_created': date, 
                                'likes': 0 ,
                                'message':request_body["message"],
                                'board_id': request_body["board_id"],
                                'author_id':request_body['user_id']})
    db.session.add(new_card)
    db.session.commit()

    return make_response(jsonify(new_card.to_dict()), 201)

# Get information on a card by ID [GET] 200 will come automatically
@bp.route("/<id>", methods=["GET"])
def read_card(id):
    card = validate_model(Card, id)
    return card.to_dict()
    
# Get information on all cards associated with a board [GET]
@bp.route("/board/<board_id>", methods=["GET"])
def read_all_cards_on_board(board_id):
    board = validate_model(Board, board_id)
    
    cards = board.cards

    cards_response = []

    for card in cards:
        cards_response.append(card.to_dict())
    
    return jsonify(cards_response)


# Update information on a card [PUT] &[PATCH]
@bp.route("/<id>", methods=["PUT"])
def update_card(id):
    card = validate_model(Card, id)
    request_body = request.get_json()

    card.message = request_body["message"]
    db.session.commit()
    return jsonify(card.to_dict())


@bp.route("/<id>/like", methods=["PATCH"])
def update_card_likes(id):
    card = validate_model(Card, id)
    card.likes += 1

    db.session.commit()
    return jsonify(card.to_dict())


# Delete card from database / board [DELETE]
@bp.route("/<id>", methods=["DELETE"])
def delete_card(id):
    card = validate_model(Card, id)
    db.session.delete(card)
    db.session.commit()
    return make_response(f"card {id} deleted", 200)