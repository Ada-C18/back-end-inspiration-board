from flask import Blueprint, request, jsonify, make_response
from app import db

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("boards", __name__, url_prefix="/boards")

#Create board (POST)

#Read board (GET)

#Read all boards? (GET)



#Delete board (DELETE)
