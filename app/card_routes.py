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

    return jsonify([card.to_dict() for card in cards])

# ===================================
#        DELETE ONE CARD BY ID
# ===================================


@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    delete_message = f'Card {card_id} successfully deleted'
    return delete_message, 200
