from flask import Blueprint, jsonify, make_response, request, abort
import requests
from app import db
from app.models.card import Card

card_bp = Blueprint("cards", __name__, url_prefix="/cards")




# GET requests for Card
@card_bp.route("", methods = ['GET'])
def get_all_cards():
    cards = Card.query.all()

    all_cards = [card.to_dict() for card in cards]

    return jsonify(all_cards)
