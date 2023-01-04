from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
from .routes_helper import get_one_obj_or_abort

card_bp = Blueprint("card",__name__, url_prefix="/card")
@card_bp.route("", methods=['POST'])
def add_card():
    request_body = request.get_json()
    new_card = Card.from_dict(request_body)

    db.session.add(new_card)
    db.session.commit()

    return {
        "message": f"Successfully created new card with id: {new_card.card_id}"
    }, 201



