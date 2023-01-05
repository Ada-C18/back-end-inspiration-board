from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card


cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")
def validate_cards(card_id):
    try:
        card_id = int(card_id)
    except:
        abort(make_response({"details": f"{card_id}: invalid data"}, 400))
    card = Card.query.get(card_id)
    if not card:
        abort(make_response({"message": f"card {card_id} not found"}, 404))
    return card

@cards_bp.route("", methods=["POST"])
def create_card():
    try:
        request_body = request.get_json()
        new_card = Card(
            id = request_body["card_id"],
            message = request_body["message"],
            like_count = request_body["is_like"],)
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400
    db.session.add(new_card)
    db.session.commit()


@cards_bp.route("/<card_id>", methods=["Delete"])
def delete_card(card_id):
    card = validate_cards(card_id)
    db.session.delete(card)
    db.session.commit()
    return make_response({"details": f"Card {card_id} successfully deleted"}), 200

@cards_bp.route("/<card_id>/like", methods=["PATCH"])
def like_card(card_id):
    card = validate_cards(card_id)
    card.like_count += 1
    db.session.add(card)
    db.session.commit()
    response_body= {}
    response_body['card']= card.to_dict()
    return jsonify(response_body), 200