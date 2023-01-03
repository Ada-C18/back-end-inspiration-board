from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(jsonify({"message":f"{cls.__name__} {model_id} not found"}), 404))
    
    return model

#### Card Routes #####

cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

# DELETE /cards/<card_id>
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    pass

# PATCH /cards/<card_id>/like
@cards_bp.route("/<card_id>/like", methods=["PATCH"])
def add_like_card(card_id):
    pass

