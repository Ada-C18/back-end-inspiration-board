from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.routes.board_routes import validate_model

card_bp = Blueprint('card_bp', __name__, url_prefix='/cards')

@card_bp.route("/<card_id>", methods=["PUT"])
def change_card_likes(card_id):
    card = validate_model(Card, card_id)
    
    request_body = request.get_json(card_id)
    card.update(request_body)

    db.session.commit()

    return make_response({
        "id": card.card_id,
        "message": card.message,
        "likes": card.likes_count
                          }), 200

@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response({
        f"details": f'Card {card_id} successfully deleted'
    }), 200