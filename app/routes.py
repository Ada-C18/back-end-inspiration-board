from flask import Blueprint, request, jsonify, make_response
from app import db

# example_bp = Blueprint('example_bp', __name__)

#Blueprints for Boards
#Blueprints for Cards

#Endpoints
#GET - /boards
#POST -/boards
#GET - /boards/<board_id>/cards
#POST - /boards/<board_id>/cards
#DELETE - /cards/<card_id>
#PUT - /cards/<card_id>/like