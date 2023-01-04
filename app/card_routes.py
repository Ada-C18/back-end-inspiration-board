from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board

cards_bp = Blueprint("cards", __name__, url_prefix="/boards/<board_id>/cards") 

def validate_model(cls, model_id):
    try: 
        model_id = int(model_id)
    except:
        abort(make_response({
            "message": f"{cls.__name__} {model_id} invalid"}, 400))
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({
            "message": f"{cls.__name__} {model_id} not found"}, 404))
    return model

@cards_bp.route("", methods=["GET"])
def read_all_cards(board_id):
    board = validate_model(Board, board_id)
    cards = board.cards
    return jsonify([card.from_instance_to_dict() for card in cards]), 200

@cards_bp.route("", methods=["POST"])
def create_card(board_id):
    #board = validate_model(Board, board_id)
    request_body = request.get_json()
    try: 
        new_card= Card.from_dict_to_instance(request_body)
    except:
        abort(make_response({"details": "invalid data" }, 400))
    #board.cards.append(new_card)
    new_card.board_id = board_id
    db.session.add(new_card)
    db.session.commit()
    return jsonify({"card created": new_card.from_instance_to_dict()}), 201

'''
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    tasks_id_list = request_body["task_ids"]
    for task_id in tasks_id_list:
        task = validate_model(Task, task_id)
        task.goal_id = goal_id
        db.session.commit()
    return {"id": goal.goal_id, "task_ids" : tasks_id_list}

@goals_bp.route("<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)
        db.session.commit()
    return make_response(jsonify({
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
        })), 200

    '''