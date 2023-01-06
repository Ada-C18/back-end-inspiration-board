from flask import Blueprint, json, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from .validation import get_one_obj_or_abort
import requests
import os

# example_bp = Blueprint('example_bp', __name__)
cards_bp = Blueprint('cards',  __name__ , url_prefix='/cards') 

# @cards_bp.route('', methods=['POST'])
# def create_one_card():
#     request_body = request.get_json()
#     try:
#         new_card = Card(message=request_body['message'])
#     except KeyError:
#         return jsonify({"details": "Invalid data"}), 400
#     db.session.add(new_card)
#     db.session.commit()
#     return jsonify(new_card.to_dict()), 201
    

# @cards_bp.route('', methods=['GET'])
# def get_all_cards():
#     card_response = []
#     cards = Card.query.all()  
#     for card in cards:
#         card_response.append(card.to_dict()) 
#     return jsonify(card_response), 200


@cards_bp.route('/<card_id>', methods=['DELETE'])
def delete_one_card(card_id):
    chosen_card = get_one_obj_or_abort(Card, card_id)
    db.session.delete(chosen_card)
    db.session.commit()
    return jsonify({
        "details": f"Card {chosen_card.card_id} \"{chosen_card.message}\" successfully deleted"
    })



