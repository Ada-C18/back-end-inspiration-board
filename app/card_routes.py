from flask import Blueprint, request, jsonify, make_response, abort
from app.models.card import Card
from app import db

cards_bp = Blueprint('cards_bp', __name__, url_prefix= '/cards')

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details": "Invalid Data"}, 400))
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details": f"{cls.__name__} {model_id} not found"}, 404))
    return model 

@cards_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()
    if len(request_body) != 1:
        return {"details": "Invalid Data"}, 400
    new_card = Card.from_dict_to_object(request_body)

    db.session.add(new_card)
    db.session.commit()

    return make_response(jsonify({"card": new_card.to_dict()}), 201)





