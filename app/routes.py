from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.card import Card
from app.models.board import Board

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

        


def validate_id(cls, id):
    try: 
        id = int(id)
    except:
        abort(make_response ({"message":f"{cls.__name__}{id} invalid"}, 400))

    obj = cls.query.get(id)

    if not obj:
        abort(make_response({"message":f"{cls.__name__} {id} not found"}, 404))

    return obj

@cards_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    card = validate_id(Card, card_id)

    return {
        "message": card.message
    }

@cards_bp.route("/<id>",methods=["DELETE"])
def delete_card(id):
    card=validate_id(Card,id)
    db.session.delete(card)
    db.session.commit()
    return make_response({"details":f'Card {id} " {card.message} "  successfully deleted'})

boards_bp = Blueprint("boards",__name__, url_prefix="/boards")