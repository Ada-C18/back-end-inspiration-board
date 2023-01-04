from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board

cards_bp = Blueprint("cards", __name__, url_prefix="/boards/<board_id>/cards") 

def validate_model(cls, model_id):
    try: 
        model_id = int(model_id)
    except:
        abort(make_response({
            "message": f"{cls.__name__} {model_id} invalid"}, 400))
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({
            "message": f"{cls.__name__} {model_id} not found"}, 404))
    return model

@cards_bp.route("", methods=["GET"])
def read_all_cards(board_id):
    board = validate_model(Board, board_id)
    cards = board.cards
    return jsonify([card.from_instance_to_dict() for card in cards]), 200

@cards_bp.route("", methods=["POST"])
def create_card(board_id):
    request_body = request.get_json()
    try: 
        new_card= Card.from_dict_to_instance(request_body)
    except:
        abort(make_response({"details": "invalid data" }, 400))
    new_card.board_id = board_id
    db.session.add(new_card)
    db.session.commit()
    return jsonify({"card created": new_card.from_instance_to_dict()}), 201

@cards_bp.route("/<card_id>", methods=["PUT"])
def update_one_card(board_id, card_id):
    card = validate_model(Card, card_id)
    request_body = request.get_json()
    card.message = request_body["message"]
    db.session.commit()
    return jsonify({"card updated": card.from_instance_to_dict()}), 200

@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(board_id, card_id):
    card = validate_model(Card, card_id)
    db.session.delete(card)
    db.session.commit()
    return jsonify({"details": f"card {card.message} has been deleted"}), 200