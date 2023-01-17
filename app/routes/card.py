from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card

bp = Blueprint("card_bp", __name__, url_prefix="/cards")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

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

    return {"details": f"Card {card.card_id} successfully deleted"}


@bp.route("<card_id>/like", methods=["PUT"])
def increase_likes(card_id):
    card = validate_model(Card, card_id)

    request_body = request.get_json()
    card.likes_count = request_body["likes_count"]
    db.session.commit()

    return make_response(jsonify({"card": card.to_dict()}), 200)


@bp.route("", methods=["GET"])
def read_all_cards():
    sort_query = request.args.get("sort")
    card_query = Card.query
    if sort_query == "asc":
        card_query = Card.query.order_by(Card.message.asc())
    if sort_query == "likes":
        card_query = Card.query.order_by(Card.likes_count.desc()) 
    cards = card_query.order_by(Card.card_id).all() 
    card_response = [card.to_dict() for card in cards]
    
    return jsonify(card_response), 200