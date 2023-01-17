from app import db
from app.models.card import Card
from app.routes.routes_helper import validate_model, validate_input_data, error_message
from flask import Blueprint, request, jsonify, make_response


cards_bp = Blueprint('cards_bp', __name__, url_prefix = '/cards')

# update likes count
@cards_bp.route("/<id>/like", methods=["PATCH"])
def like_card(id):
    card = validate_model(Card, id)
    card.likes_count += 1
    db.session.commit()

    return make_response(jsonify(card.to_dict()), 200)

# delete card:
@cards_bp.route("/<id>", methods=["DELETE"])
def delete_card(id):
    print(id)
    card = validate_model(Card, id)

    db.session.delete(card)
    db.session.commit()

    return jsonify({"details": f"Card {id} successfully deleted"}), 200

