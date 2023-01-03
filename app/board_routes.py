from flask import Blueprint, request, jsonify, make_response
from .card_routes import validate_model
from app.models.card import Card
from app.models.board import Board
from app import db

board_bp = Blueprint('board_bp', __name__, url_prefix='/boards')




@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if len(request_body) != 2:
        return {"details": "Invalid Data"}, 400
    new_board = Board.from_dict_to_object(request_body)

    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify({"board": new_board.to_dict()}), 201)

# @tasks_bp.route("", methods=["GET"])
# def read_all_tasks():
#     title_query = request.args.get('title')
#     sort_query = request.args.get('sort')

#     if title_query:
#         tasks = Task.query.filter_by(title=title_query)
        
#     if sort_query == "asc":
#         tasks = Task.query.order_by(Task.title.asc())
        
#     if sort_query == "desc":
#         tasks = Task.query.order_by(Task.title.desc())
        
#     if not title_query and not sort_query:
#         tasks = Task.query.all()
#     tasks_response = [task.to_dict() for task in tasks]
#     return jsonify(tasks_response)


