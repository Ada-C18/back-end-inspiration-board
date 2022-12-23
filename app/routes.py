from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.card import Card


def get_one_obj_or_abort(cls, obj_id):
    try:
        obj_id = int(obj_id)
    except ValueError:
        abort(make_response({"message":f"Invalid {cls.__name__} ID: `{obj_id}`. ID must be an integer"}, 400))

    matching_obj = cls.query.get(obj_id)

    if not matching_obj:
        abort(make_response({"message":f"{cls.__name__} with id `{obj_id}` was not found in the database."}, 404))

    return matching_obj

card_bp = Blueprint('card_bp', __name__, url_prefix='/cards')

@card_bp.route("", methods=["POST"])
def add_card():
    request_body = request.get_json()

    new_card = Card.from_json(request_body)

    db.session.add(new_card)
    db.session.commit()

    return {"card": new_card.to_json()}, 201


@card_bp.route("", methods=["GET"])
def get_all_cards():
    cards = Card.query.all()

    cards_response = [card.to_json() for card in cards]

    return jsonify(cards_response)


@card_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    chosen_card = get_one_obj_or_abort(Card, card_id)

    card_json = chosen_card.to_json()

    return jsonify(card_json), 200


@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    chosen_card = get_one_obj_or_abort(Card, card_id)

    db.session.delete(chosen_card)

    db.session.commit()

    return jsonify({"message": f"Successfully deleted card with id `{card_id}`"}), 200
