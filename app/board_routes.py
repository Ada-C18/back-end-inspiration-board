from flask import Blueprint, request, jsonify, make_response
from app import db

board_bp = Blueprint("board",__name__,url_prefix = "/boards")

#Read ALL boards
@board_bp.route("/", strict_slashes=False, methods="GET")

#Delete Board
@board_bp.route("/", strict_slashes=False, methods="DELETE")

#Update Board
@board_bp.route("/<board_id>", strict_slashes=False, methods="PUT")

#Create Board
@board_bp.route("/", strict_slashes=False, methods="POST")

#Read ALL cards
@board_bp.route("/<board_id>/cards", strict_slashes=False, methods="GET")