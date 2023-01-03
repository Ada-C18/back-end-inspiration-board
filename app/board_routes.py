from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
import os, requests

# creating blueprint
board_bp = Blueprint("Board", __name__, url_prefix="/boards")

# Create a board/post


