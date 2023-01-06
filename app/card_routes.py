from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
from app.validate_data import validate_model

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")



#======================================
#        GET ALL CARDS
#======================================


@cards_bp.route("", methods=["GET"])
def read_all_cards():

    cards = Card.query.all()

    cards_response = []  # returns empty list if no cards

    for card in cards:
        cards_response.append({
            "card_id": card.card_id,
            "message": card.message,
            "likes_count": card.likes_count,
            "board_id": card.board_id
        })

    return jsonify(cards_response), 200

# ===================================
#        DELETE ONE CARD BY ID
# ===================================


@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card, card_id)

    # update database?
    # db.session.delete(card)
    # db.session.commit()

    # return delete message to user
    delete_message = f'Card {card_id} successfully deleted'
    return delete_message, 200

# ===================================
#        LIKE (UPDATE) ONE CARD 
# ===================================
@cards_bp.route("/<card_id>/like", methods=["PUT"])
def like_card(card_id):
    card = validate_model(Card, card_id)
    request_body = request.get_json()
    card.likes_count += 1
    
    db.session.commit()
    
    return make_response("card liked", 200)

###########################

@cards_bp.route("/<card_id>/like", methods=["PUT"])
def update_card(card_id):
    card = validate_model(Card, card_id)
    
    request_body = request.get_json()
    
    card.message = request_body["message"]
    card.likes_count = request_body["likes_count"]
    
    