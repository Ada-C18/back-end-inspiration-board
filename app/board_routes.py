from  app import db
from app.models.board import Board
from flask import Blueprint, request, jsonify, make_response

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
