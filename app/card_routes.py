from app import db
from app.models.board import Board
from app.models.card import Card
from app.board_routes import validate_model
from flask import Blueprint, request, jsonify, make_response

cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

# DELETE /cards/<card_id>
# PUT /cards/<card_id>/like

@cards_bp.route("/<card_id>/like", methods=["PUT"])
def update_like_cards(card_id):
    card = validate_model(Card, card_id)
    request_body = request.get_json()
    
    card.likes_count = request_body["likes_count"]
    
    db.session.commit()

    return make_response(jsonify(card.to_dict()), 201)

@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card, card_id)
    
    db.session.delete(card)
    db.session.commit()
    
    return make_response(jsonify(card.to_dict()), 200)