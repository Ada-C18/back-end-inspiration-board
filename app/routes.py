from flask import Blueprint, request, jsonify, make_response
from app import db

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


#create a get route 
#@boards_bp.route


#create a post route 



#create a route to delete a card



#create a route to delete all boards and cards 



# response bodies must have title, owner, and board_id 

