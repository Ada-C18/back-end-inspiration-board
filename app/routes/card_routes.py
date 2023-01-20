from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board

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

# UPDATE heart count on a card
@cards_bp.route("/<card_id>", methods = ["PUT"])
def update_likes(card_id):
    card = Card.query.get(card_id)
    request_body = request.get_json()
    card.likes_count = request_body["likes_count"]
 
    db.session.commit()

    return make_response(f"Card #{card_id} successfully updated")

#Delete
@cards_bp.route("/<card_id>", methods = ["DELETE"])
def delete_card(card_id):
    card = Card.query.get(card_id)
    db.session.delete(card)
    db.session.commit()
    return make_response(f"Card #{card_id} successfully deleted", 200)

# Delete all cards
@cards_bp.route("", methods = ["DELETE"])
def delete_all_cards():
    cards = Card.query.all()
    for card in cards:
        db.session.delete(card)
    db.session.commit()
    return make_response("All cards successfully deleted")