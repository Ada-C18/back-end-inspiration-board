from flask import Blueprint, request, jsonify, make_response, abort
from app import db

bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

# Create a card [POST]

# Get information on a card by ID [GET]
# Get information on all cards associated with a board [GET]

# Update information on a card [PATCH]

# Delete card from database / board [DELETE]