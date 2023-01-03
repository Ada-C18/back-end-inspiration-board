# helper function to get a card by id:
from app.models.card import Card
from flask import abort, make_response

def get_card_from_id(card_id):
    try:
        card_id = int(card_id)
    except ValueError:
        return abort(make_response({"msg":f"Invalid data type: {card_id}"}, 400))
    chosen_card = Card.query.get(card_id)

    if chosen_card is None:
        return abort(make_response({"msg": f"Could not find card item with id: {card_id}"}, 404))
    return chosen_card
