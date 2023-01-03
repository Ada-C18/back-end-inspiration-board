from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card


# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")
card_bp = Blueprint("card_bp", __name__, url_prefix="/cards")

# @books_bp.route("", methods=["POST"])
# def create_books():
#     request_body = request.get_json()
#     new_book = Book(title=request_body["title"],
#                     description=request_body["description"])

#     db.session.add(new_book)
#     db.session.commit()

#     # return make_response(f"Book {new_book.title} successfully created", 201)
#     return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)

@card_bp.route("", methods=["POST"])
def create_card():
    response_body = request.get_json()
    
    new_card = Card.from_dict(response_body)
    db.session.add(new_card)
    db.session.commit()

    return {"card_id": new_card.card_id}, 201

# @task_bp.route("", methods=["GET"])
# def get_all_tasks():