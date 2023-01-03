from app import db
from app.models.board import Board
from app.models.card import Card
from flask import Blueprint, request, jsonify, make_response, abort

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model