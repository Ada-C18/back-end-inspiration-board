from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)

cards_bp = Blueprint("cards",__name__, url_prefix="/cards")

@cards_bp.route("", methods=["POST", "GET"])
def get_or_post_cards():
    if request.method=="GET":
        cards=Card.query.all()
        cards_response=[]
        for card in cards:
            cards_response.append({
                "id":card.id,
                "message":card.message
            })
        return jsonify(cards_response)
    
    elif request.method =="POST" :
        request_body=request.get_json()
        new_card = Card(message= request_body["message"])

        db.session.add(new_card)
        db.session.commit()

        return make_response(f"Card {new_card.message} successfully created", 201)


