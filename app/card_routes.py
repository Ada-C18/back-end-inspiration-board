from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board
import os, requests
from app.board_routes import validate_model

# Card
# CREATE a new card to a board
# READ all cards belonging to a board
# UPDATE ‘+1’s for a card
# DELETE a card


# creating blueprint
card_bp = Blueprint("Card", __name__, url_prefix="/cards")

# def validate_model(cls, model_id):
#     try:
#         model_id = int(model_id)
#     except:
#         abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

#     model = cls.query.get(model_id)
#     if not model:
#         abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

#     return model
# # create a card
# @card_bp.route("boards/<board_id>", methods=["POST"])
# def create_card():
#     request_body = request.get_json()

#     if not all(["message" in request_body, "likes_count" in request_body]):
#         return {"details" : "Invalid data: Please provide a message and likes count"}, 400

#     new_card = Card.from_dict(request_body)

#     db.session.add(new_card)
#     db.session.commit

#     return {"card": new_card.to_dict()}, 201

# read all cards