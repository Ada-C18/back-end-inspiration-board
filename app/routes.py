from flask import Blueprint, request, jsonify, make_response
from app import db

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")