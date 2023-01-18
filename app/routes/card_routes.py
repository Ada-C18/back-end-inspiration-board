from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# GET all cards
@cards_bp.route("", methods = ["GET"])
def get_all_cards():
    cards = Card.query.all()
    cards_response = []
    for card in cards:
        cards_response.append(
            {
              "card_id": card.card_id,
              "message": card.message,
              "likes": card.likes_count,
              "board_id": card.board_id  
            }
        )
    return jsonify(cards_response)

# # POST create new card
# @cards_bp.route("/<board_id>", methods = ["POST"])
# def create_card(board_id):
#     # board = Board.query.get(board_id)
#     request_body = request.get_json()
    
#     if "message" not in request_body:
#         return jsonify({"message": "Message cannot be blank!"}, 400)
#     if len(request_body["message"]) > 40:
#         return jsonify({"message": "Maximum length 40 characters."}, 400)

#     new_card = Card(
#         board_id = board_id,
#         message = request_body["message"],
#         likes_count = 0
#     )

#     db.session.add(new_card)
#     db.session.commit()
    
#     return make_response(jsonify({"card": new_card.message}), 201)

# UPDATE heart count on a card
@cards_bp.route("/<card_id>", methods = ["PATCH"])
def update_likes(card_id):
    card = Card.query.get(card_id)
    request_body = request.get_json()
    card.likes_count = request_body["likes_count"]
 
    db.session.commit()

    return make_response(f"Book #{card_id} successfully updated")

#Delete
@cards_bp.route("/<card_id>", methods = ["DELETE"])
def delete_card(card_id):
    card = Card.query.get(card_id)
    db.session.delete(card)
    db.session.commit()

# @cards_bp.route("", methods = ["DELETE"])
# def delete_all_cards():
#     card = Card.query.
