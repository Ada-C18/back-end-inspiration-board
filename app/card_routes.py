from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# validate_model
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"invalid model id {model_id}"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"model id {model_id} not found"}, 404))
    
    return model

# delete a card
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card, card_id)
    
    db.session.delete(card)
    db.session.commit()
    
    return make_response("success deleting",200)

# like a card
@cards_bp.route("/<card_id>/like", methods=["PUT"])
def like_card(card_id):
    card = validate_model(Card, card_id)
    card.likes_count += 1
    
    db.session.commit()
    
    return make_response("success liking",200)