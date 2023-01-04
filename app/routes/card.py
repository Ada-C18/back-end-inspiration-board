from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card

bp = Blueprint("card_bp", __name__, url_prefix="/card")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


@bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()
    new_card = Card.from_dict(request_body)

    db.session.add(new_card)
    db.session.commit()

    card_dict = new_card.to_dict()

    return make_response(jsonify({"card": card_dict}), 201)

@bp.route("<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return {"details": f'Card {card.card_id} successfully deleted'}
