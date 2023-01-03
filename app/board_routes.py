from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board
from .card_routes import validate_model

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

