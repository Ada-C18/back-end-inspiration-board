from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card

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
              "likes": card.likes_count  
            }
        )
    return jsonify(cards_response)

# POST create new card
@cards_bp.route("", methods = ["POST"])
def create_card():
    request_body = request.get_json()
    new_card = Card(
        message = request_body["message"],
        likes_count = 0
    )

    db.session.add(new_card)
    db.session.commit()
    
    return make_response(jsonify({"card": new_card.message}), 201)

# UPDATE heart count on a card
@cards_bp.route("/<card_id>", methods = ["PATCH"])
def update_likes(card_id):
    card = Card.query.get(card_id)
    card.likes_count += 1
    db.session.commit()

    

#Delete
@cards_bp.route("", methods = ["DELETE"])
def delete_card(card_id):
    card = Card.query.get(card_id)
    db.session.delete(card)
    db.session.commit()