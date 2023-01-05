from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card


cards_bp = Blueprint('cards_bp', __name__, url_prefix = '/cards')
def validate_card(card_id):
    try:
        card_id = int(card_id)
    except:
        abort(make_response({"message":f"card {card_id} invalid"},400))

    card = Card.query.get(card_id)

    if not card:
        abort(make_response({"message":f"card {card_id} not found"}, 404))

    return card

@cards_bp.route("",methods=["POST"])
def create_cards():
    request_body = request.get_json()
    new_card = Card(message=request_body['message'],
    likes_count = request_body['likes_count'])

    db.session.add(new_card)
    db.session.commit()

    return make_response(f"Card {new_card.message} successfully created", 201)


# Current GET route for showing cards associated with a board is url/boards/id, do we still need this route?
@cards_bp.route("", methods=["GET"])
def get_cards():
    cards_response = []
    cards = Card.query.all()
    for card in cards:
        cards_response.append({
            'id': card.id,
            'message': card.message,
            'likes_count': card.likes_count
        })
    
    return jsonify(cards_response)


# do we need this route? 
@cards_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    card = validate_card(card_id)
    return {
            'id': card.id,
            'message': card.message,
            'likes_count': card.likes_count
    }


@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_card(card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response(f"card #{card.id} successfully deleted ")
