from app import db
from app.models.board import Board
from app.models.card import Card
from flask import Blueprint, request, jsonify, make_response

cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")