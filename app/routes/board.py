from flask import Blueprint, request, jsonify, make_response,abort
from app import db
from app.models.board import Board

board_bp = Blueprint("board_bp", __name__, url_prefix="/board")

def validate_board_id(board_id):
    try:
        board_id = int(board_id)
    except ValueError:
        abort(make_response(jsonify({"message": "board_id must be an integer"}),400))
    
    matching_board = Board.query.get(board_id)

    if matching_board is None:
        response_str = f"Board with id {board_id} was not found in the database."
        abort(make_response(jsonify({"message": response_str}), 404))

    return matching_board


@board_bp.route("", methods = ["POST"])
def add_board():
    request_body = request.get_json()
    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}),400

    new_board = Board(title=request_body["title"])

    db.session.add(new_board)
    db.session.commit()

    board_dict = new_board.to_dict()

    return jsonify({"board":board_dict}),201

@board_bp.route("", methods=["GET"])
def get_all_boards():

    title_query = request.args.get("title")
    sort_at_query = request.args.get("sort")

    if title_query:
        boards = Board.query.filter_by(title = title_query)
    elif sort_at_query == "asc":
        boards = Board.query.order_by(Board.title)
    elif sort_at_query == "desc":
        boards = Board.query.order_by(Board.title.desc())
    else:
        boards = Board.query.all()
    
    response = [board.to_dict() for board in boards]

    return jsonify(response), 200

@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_board_id(board_id)

    board_dict = board.to_dict()
    
    return jsonify({"board":board_dict})

@board_bp.route("/<board_id>", methods=["PUT"])
def update_board(board_id):
    board = validate_board_id(board_id)

    request_body = request.get_json()

    if "title" not in request_body:
                return jsonify({"message":"Request must include title"}),400

    board.title = request_body["title"]

    board_dict = board.to_dict()

    db.session.commit()

    return jsonify({"board":board_dict}),200

@board_bp.route("/<board_id>",methods = ['DELETE'])
def delete_board(board_id):
    board = validate_board_id(board_id)

    db.session.delete(board)

    db.session.commit()

    return jsonify({"details":f"Board {board.board_id} \"{board.title}\" successfully deleted"}),200

@board_bp.route("/<board_id>/tasks", methods=["POST"])
def add_all_tasks_for_one_board(board_id):
    board = validate_board_id(board_id)

    request_body = request.get_json()

    if "task_ids" not in request_body:
        return jsonify({"details": "Invalid data"}),400

    board.tasks = []

    for id in request_body["task_ids"]:
        task = validate_task_id(id)
        board.tasks.append(task)

    db.session.commit()

    return jsonify({"id": board.board_id, "task_ids": request_body["task_ids"]}), 200

@board_bp.route("/<board_id>/tasks", methods=["GET"])
def get_all_tasks_for_one_board(board_id):
    board = validate_board_id(board_id)

    all_board_tasks = []

    tasks = board.tasks
    
    for task in tasks:
        all_board_tasks.append({
            "id": task.task_id, 
            "board_id": task.board_id,
            "title": task.title, 
            "description": task.description, 
            "is_complete": task.is_complete
        })

    return {
        "id": board.board_id,
        "title": board.title,
        "tasks": all_board_tasks
    }, 200
