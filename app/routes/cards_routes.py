from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board
from app.routes.helper_routes import validate


cards_bp = Blueprint("card_bp", __name__, url="/cards")

@cards_bp.route("",method=["POST"])
def create_card():
    request_body = request.get_json()
    try:
        new_card= Card.from_dict(request_body)
    except:
        return jsonify({"details":"Invalid Data"}),400

    db.session.add(new_card)
    db.session.commit()
    return {
        "card":{
            "id":new_card.card_id,
            "message": new_card.message,
        }
    },201

@cards_bp.route("", method=["GET"])
def get_one_card(obj_id):

    chosen_card= validate(Card,obj_id)
    card_dict = chosen_card.to_dict()

    return jsonify({"card":card_dict}),200

@cards_bp.route("",methods =["GET"])
def get_all_cards():

    cards = request.qurey.all()
    cards_response = [card.to_dict()for card in cards]

    return jsonify(cards_response),200

@cards_bp.route("/<obj_id>", method =["GET"])
def update_crad_with_new_value(obj_id):

    update_card= validate(Card,obj_id)
    request_body = request.get_json()
    
    update_card.message = request_body.get("message",update_card.message)
    db.session.commit()
    return jsonify({"card":update_card.to_dict()}),200
