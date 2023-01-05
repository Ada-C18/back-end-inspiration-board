from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
import datetime


card_bp = Blueprint("card_bp", __name__, url_prefix="/card")

def validate_card_id(card_id):
    try:
        card_id = int(card_id)
    except ValueError:
        abort(make_response(jsonify({"message": "card_id must be an integer"}),400))
    
    matching_card = Card.query.get(card_id)

    if matching_card is None:
        response_str = f"Card with id {card_id} was not found in the database."
        abort(make_response(jsonify({"message": response_str}), 404))

    return matching_card



@card_bp.route("", methods = ["POST"])
def create_card():
    request_body = request.get_json()
    if "message" not in request_body:
        return jsonify({"details": "Invalid data"}),400

    new_card = Card(message=request_body["message"],
                    board_id=request_body["board_id"])

    db.session.add(new_card)
    db.session.commit()

    card_dict = new_card.to_dict()

    return jsonify({"card":card_dict}),201

@card_bp.route("", methods=["GET"])
def get_all_cards():
    #filter based off on parameter, optional
    # DO WE FILTER HERE OR FRONT END FOR THE ADDITIONAL FEATURE
    sort_at_query = request.args.get("sort")

    if sort_at_query == "asc":
        cards = Card.query.order_by(Card.likes_count)
    elif sort_at_query == "desc":
        cards = Card.query.order_by(Card.likes_count.desc())
    else:
        cards = Card.query.all()
    response = [card.to_dict() for card in cards]
    return jsonify(response), 200


# WHERE DO WE STORE LIKE DATA? LOCAL STATE? API CALL EVERY TIME?
@card_bp.route("/<card_id>", methods=["PUT"])
def add_like_to_card(card_id):
    card = validate_card_id(card_id)

    card.likes_count += 1
    card_dict = card.to_dict()
    
    return jsonify({"card":card_dict})



@card_bp.route("/<card_id>",methods = ['DELETE'])
def delete_card (card_id):
    card = validate_card_id(card_id)
    db.session.delete(card)
    db.session.commit()

    return jsonify({"details":f"Card {card.card_id} \"{card.message}\" successfully deleted"}),200

# IF WE WANT TIME POSTED
# @card_bp.route("/<card_id>/mark_complete",methods = ['PATCH'])
# def mark_complete_on_incomplete_task(card_id):
#     card = validate_card_id(card_id)

#     datetime_object = datetime.datetime.now()
#     card.completed_at = datetime_object
#     card.is_complete = True
#     card_dict = card.to_dict()
#     db.session.commit()
    
#     return jsonify({"card":card_dict})


