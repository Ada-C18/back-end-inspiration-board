from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.routes_board import get_model_from_id
from app.models.board import Board

cards_bp = Blueprint('cards_bp', __name__, url_prefix="/cards")

@cards_bp.route("", methods=["POST"])
def create_one_card():
  request_body = request.get_json()

  if len(request_body["message"]) > 40 or len(request_body["message"]) < 1:
    return abort(make_response({"msg": f"invalid message input"}, 404))

  if "board_id" not in request_body:
    board = None
  else:
      board = get_model_from_id(Board, request_body["board_id"])

  new_card =  Card (
      message= request_body["message"],
      likes_count=0,
      board= board
  )

  db.session.add(new_card)
  db.session.commit()

  return jsonify({"card": new_card.to_dict()}), 201

@cards_bp.route("<card_id>", methods=["GET"])
def get_one_card(card_id):
  chosen_card = get_model_from_id(Card, card_id)
  return jsonify({"card": chosen_card.to_dict()}), 200

@cards_bp.route("", methods=['GET'])
def get_all_cards():
  cards = Card.query.all()
  result = []
  for card in cards:
    result.append(card.to_dict())

  return jsonify(result), 200

@cards_bp.route("<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
  card_to_delete = get_model_from_id(Card, card_id)
  message_card_to_delete = get_model_from_id(Card, card_id).to_dict()["message"]

  db.session.delete(card_to_delete)
  db.session.commit()

  return jsonify({"msg": f"card '{message_card_to_delete}' deleted"}), 200

@cards_bp.route("<card_id>", methods=["PATCH"])
def add_like_to_card(card_id):
  card_to_update = get_model_from_id(Card, card_id)
  card_to_update.add_likes()
  card_likes = get_model_from_id(Card, card_id).to_dict()["likes_count"]

  db.session.commit()
  return jsonify({"msg": f"card updated to {card_likes} likes"}), 200


