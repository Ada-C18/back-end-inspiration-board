from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
import os, requests

# creating blueprint
card_bp = Blueprint("Card", __name__, url_prefix="/cards")

# create a card
