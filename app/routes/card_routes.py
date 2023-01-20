from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
from .routes_helper import get_one_obj_or_abort

card_bp = Blueprint("card",__name__, url_prefix="/card")

@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    chosen_card = get_one_obj_or_abort(Card, card_id)

    db.session.delete(chosen_card)

    db.session.commit()

    return jsonify({
        "message": f"Successfully deleted card with id: {card_id}"
    }), 200

# @card_bp.route("/<card_id>/<inc_or_dec>", methods=["PATCH"])
# def update_likes_for_one_card(card_id, inc_or_dec):
#     chosen_card = get_one_obj_or_abort(Card, card_id)
#     if chosen_card.likes_count is None:
#         chosen_card.likes_count = 0
#     if inc_or_dec == "inc":
#         chosen_card.likes_count+=1
#     if inc_or_dec == "dec" and chosen_card.likes_count > 0:
#         chosen_card.likes_count-=1

#     db.session.commit()
#     return jsonify({"message": f"Successfully updated the likes count for Card ID {card_id}"}), 200

@card_bp.route("/<card_id>", methods=["PATCH"])
def update_likes_for_one_card(card_id):
    chosen_card = get_one_obj_or_abort(Card, card_id)
    request_body= request.get_json()

    chosen_card.likes_count = request_body["likes_count"]

    db.session.commit()

    return jsonify({"message": f"Successfully updated the likes count for Card ID {card_id}"}), 200

