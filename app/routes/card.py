from flask import Blueprint, request, jsonify, make_response
from app import db

bp = Blueprint("card_bp", __name__, url_prefix="/card")
