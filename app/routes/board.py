from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

boards_bp = Blueprint('boards_bp', __name__, url_prefix = '/boards')
