from flask import Blueprint, jsonify, make_response, request, abort
# import requests
from app import db
from app.models.card import Card

card_bp = Blueprint("cards", __name__, url_prefix="/cards")


def validate_model(cls, model_id):
    try:
        model_id=int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__}{model_id} invalid"}, 400))
    model =  cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))
    return model

# GET requests for Card
@card_bp.route("", methods = ['GET'])
def get_all_cards():
    cards = Card.query.all()

    all_cards = [card.to_dict() for card in cards]

    return jsonify(all_cards)

@card_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    card = validate_model(Card, card_id)
    return {"card": card.to_dict()}, 200

@card_bp.route("", methods=["POST"])
def create_card():
    try:
        request_body = request.get_json()

        new_card = Card.from_dict(request_body)

    except:
        abort(make_response({"details": "Invalid data"}, 400 ))

    db.session.add(new_card)
    db.session.commit()

    return {"card": new_card.to_dict()}, 201

@card_bp.route("/<card_id>", methods=["PATCH"])
def update_card_likes(card_id):

    card = validate_model(Card, card_id)
    request_body = request.get_json()
    card.likes_count += 1
    db.session.commit()
    return {"card": card.to_dict()}, 200

@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card, card_id)
    db.session.delete(card)
    db.session.commit()
    return make_response(jsonify({"details": f'Card {card.card_id} successfully deleted'}),200)
