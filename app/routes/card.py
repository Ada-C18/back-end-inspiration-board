from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card

card_bp = Blueprint("card_bp", __name__, url_prefix="/card")

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response(jsonify({"message": "task_id must be an integer"}),400))
    
    matching_task = Task.query.get(task_id)

    if matching_task is None:
        response_str = f"Task with id {task_id} was not found in the database."
        abort(make_response(jsonify({"message": response_str}), 404))

    return matching_task

def slack_call(msg):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_TOKEN")

    query_params = {
        "channel": "task-notifications",
        "text": msg
    }

    header = {
        "Authorization": "Bearer " + SLACK_API_KEY
    }

    requests.post(PATH, params=query_params, headers=header)

@task_bp.route("", methods = ["POST"])
def add_task():
    request_body = request.get_json()
    if "title" not in request_body or \
        "description" not in request_body:
        return jsonify({"details": "Invalid data"}),400

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    task_dict = new_task.to_dict()

    return jsonify({"task":task_dict}),201

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    #filter based off on parameter, optional
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_at_query = request.args.get("completed_at")
    sort_at_query = request.args.get("sort")

    if title_query:
        tasks = Task.query.filter_by(title = title_query)
    elif description_query:
        tasks = Task.query.filter_by(description = description_query)
    elif completed_at_query:
        tasks = Task.query.filter_by(completed_At = completed_at_query)
    elif sort_at_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_at_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    response = [task.to_dict() for task in tasks]
    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task_id(task_id)
    task_dict = task.to_dict()
    
    return jsonify({"task":task_dict})

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
                return jsonify({"message":"Request must include title and description"}),400

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    task_dict = task.to_dict()

    return jsonify({"task":task_dict}),200

@task_bp.route("/<task_id>",methods = ['DELETE'])
def delete_task(task_id):
    task = validate_task_id(task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({"details":f"Task {task.task_id} \"{task.title}\" successfully deleted"}),200

@task_bp.route("/<task_id>/mark_complete",methods = ['PATCH'])
def mark_complete_on_incomplete_task(task_id):
    task = validate_task_id(task_id)

    datetime_object = datetime.datetime.now()
    task.completed_at = datetime_object
    task.is_complete = True
    task_dict = task.to_dict()
    db.session.commit()
    
    slack_call(f"Someone just completed the task {task.title}")

    return jsonify({"task":task_dict})

@task_bp.route("/<task_id>/mark_incomplete",methods = ['PATCH'])
def mark_incomplete_on_complete_task(task_id):
    task = validate_task_id(task_id)

    task.completed_at = None
    task.is_complete = False
    task_dict = task.to_dict()
    
    db.session.commit()

    return jsonify({"task":task_dict})


