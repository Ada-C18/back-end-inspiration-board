from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.user import User

bp = Blueprint("users_bp", __name__, url_prefix="/users")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    return model

@bp.route("", methods=["POST"])
def create_user():
    request_body = request.get_json()

    if request_body["name"] == "":
        abort(make_response({"message":"Please include a name"}, 400))

    users = User.query.all()

    for user in users:
        if request_body["name"] == user.name:
            abort(make_response({"message":f"{request_body['name']} is taken. Please choose another name."}, 404))

    new_user = User(name=request_body["name"])

    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify(f"User {new_user.name} successfully created"), 201)

@bp.route("", methods=["GET"])
def read_all_users():
    users = User.query.all()

    users_response = []
    for user in users:
        users_response.append(
            {
                "name": user.name
            }
        )
    return jsonify(users_response)