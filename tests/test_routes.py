from werkzeug.exceptions import HTTPException
from app.board_routes import validate_model
from app.models.board import Board
from app.models.card import Card
import pytest

