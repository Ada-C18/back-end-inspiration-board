from app.models.user import User
from app.models.board import Board
from app.models.card import Card
import pytest

def test_create_user_no_missing_data():
    name = "Test"

    result = User(name=name)

    assert result["id"] == 1
    assert result["name"] == "Test"

def test_create_user_missing_name():
    name = None

    with pytest.raises(KeyError, match = 'name'):
        new_user = User(name=name)


def test_board_to_dict_no_missing_data():
    user = User(name="Tester")
    test_data = Board(id = 1, date_created = "Date is right now", title = "Test Pass Please", visible=True, owner = user.name)

    result = test_data.to_dict()

    assert len(result) == 6
    assert result["id"] == 1
    assert result["title"] == "Test Pass Please"
    assert result["date_created"] == "Date is right now"

def test_board_to_dict_missing_id():
    user = User(name="Tester")
    test_data = Board(title="This is missing it's ID", date_created="Date is right now", visible=True, owner=user.name)

    result = test_data.to_dict()

    assert len(result) == 6
    assert result["id"] is None
    assert result["title"] == "This is missing it's ID"

def test_board_to_dict_missing_title():
    user = User(name="Tester")
    title = None

    with pytest.raises(KeyError, match = "title"):
        new_board = Board(title = title, date_created="Date is right now", visible=True, owner=user.name)

def test_board_to_dict_missing_owner():
    user = None

    with pytest.raises(KeyError, match = "owner"):
        new_board = Board(title = "No user should cause an error", date_created="Date is right now", visible=True, owner = user)

def test_board_from_dict_returns_board():
    user = User(name="Tester")
    board_data = {
        "title": "We're testing From Dict", "date_created": "Date is right now", "visible": True, "owner": user.name
    }

    new_board = Board.from_dict(board_data)

    assert new_board.title == "We're testing From Dict"
    assert new_board.owner == "Tester"

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

def test_from_dict_with_extra_keys():
    user = User(name="I'm so tired")
    board_data = {"title": "we have extra keys", "date_created": "Date is right now", "visible": True, "owner": user.name, "fancy": "Fancy stuff"}

    new_board = Board.from_dict(board_data)

    assert new_board.title == "we have extra keys"
    assert new_board.owner == "I'm so tired"