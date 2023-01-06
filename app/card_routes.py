from flask import Blueprint, request, jsonify, make_response, abort

from app.models.board import Board
from app.models.card import Card
from app import db

# example_bp = Blueprint('example_bp', __name__)

card_bp = Blueprint ("card", __name__, url_prefix= "/cards")

def get_validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


#Delete Card

@card_bp.route("/<card_id>", strict_slashes=False, methods=["DELETE"])
def delete_card(card_id):
    card = get_validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    response_body = {
        "message": f'Card #{card_id} was deleted.'}
    return make_response(jsonify(response_body), 200)

# Update Card
@card_bp.route("/<card_id>", strict_slashes=False, methods=["PUT"])
def update_card(card_id):
    card = get_validate_model(Card, card_id)

    request_body = request.get_json()
    card.message = request_body["message"]
    card.likes = request_body["likes"]

    db.session.commit()

    current_card_response = card.to_dict()
    return make_response(jsonify(current_card_response), 200)


#increase likes
# def increase_likes():

