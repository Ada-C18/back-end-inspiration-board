from flask import Blueprint, request, jsonify, make_response
from app.models.board import Board
from app.models.card import Card
from app import db

# example_bp = Blueprint('example_bp', __name__)
card_bp = Blueprint ("card", __name__, url_prefix= "/cards")

@card_bp.route("/", strict_slashes= False, methods=["GET"])


@card_bp.route("/<card_id>", strict_slashes= False, methods=["GET"])