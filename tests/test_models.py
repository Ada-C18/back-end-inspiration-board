from app.models.user import User
from app.models.board import Board
from app.models.card import Card
import pytest

def test_create_user_no_missing_data():
    name = "Test"

    result = User(name=name, id=1)

    assert result.id == 1
    assert result.name == "Test"

def test_board_from_dict_no_title():
    user = User(name="Tester")
    board_data = {"date_created": "Date is right now", "visible": True, "owner": user.name
    }

    with pytest.raises(KeyError, match = "title"):
        new_board = Board.from_dict(board_data)

def test_board_from_dict_no_owner():
    user = None
    board_data = {"title": "No owner here", "date_created": "Date is right now", "visible": True, "owner": user}

    with pytest.raises(KeyError, match = "owner"):
        new_board = Board.from_dict(board_data)