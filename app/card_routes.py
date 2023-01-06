from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.card import Card

card_bp = Blueprint('card_bp', __name__, url_prefix='/card')

def validate_card(card_id):
    # used to determine correct type for card search
    try:
        card_id = int(card_id)
    except:
        abort(make_response({"error message":f"{card_id} is an invalid input."}, 400))
    
    card = Card.query.get(card_id)

    # used to determine if searched card is within database
    if not card:
        abort(make_response({"error message":f"Card ID {card_id} not found."}, 404))
    
    return card

@card_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()

    # ensures minimum input for card; its message
    if "message" not in request_body:
        return make_response({"error message": "Invalid input"}, 400)

    # an attempt at managing the character limit
    if len(request_body["message"]) > 40:
        return make_response({"error message": "Input exceeds character limit."})

    # id and likes count should be automatically added
    new_card = Card(
        message = request_body["message"]
    )

    db.session.add(new_card)
    db.session.commit()
    
    return make_response({"card":new_card.to_dict()}, 201)

@card_bp.route('',methods=['GET'])
def get_cards():
    card_query = Card.query

    cards = card_query.all()

    cards_response = []
    for card in cards:
        cards_response.append({
            "card_id" : card.card_id,
            "message" : card.message,
            "likes_count" : card.likes_count,
            "board_id" : card.board_id
        })

    return jsonify(cards_response)

@card_bp.route("/<card_id>",methods=['DELETE'])
def delete_card(card_id):
    card = validate_card(card_id)
    card = Card.query.get(card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response({"details": f'Card {card_id} successfully deleted'}, 200)

@card_bp.route("/<card_id>", methods=['PATCH'])
def update_card_like_count(card_id):
    card = validate_card(card_id)
    card = Card.query.get(card_id)

    card.likes_count += 1

    db.session.commit()
    return make_response({"card":card.to_dict()}, 200)

