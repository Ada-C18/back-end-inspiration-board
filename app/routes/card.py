from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card

bp = Blueprint("card_bp", __name__, url_prefix="/card")


@bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()
    new_card = Card.from_dict(request_body)

    db.session.add(new_card)
    db.session.commit()

    card_dict = new_card.to_dict()

    return make_response(jsonify({"card": card_dict}), 201)

# @bp.route("", methods=["GET"])
# def read_cards():
