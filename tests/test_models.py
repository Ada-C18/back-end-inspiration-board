from app.models.board import Board
from app.models.card import Card
import pytest

#Write tests for to_dict and from_json methods for both boards and cards
def test_to_dict_no_missing_data():
    test_data = Board(board_id=1,
                      title="Test",
                      owner="Jane")
    
    result = test_data.to_dict()

    assert len(result) == 4
    assert result["board_id"] == 1
    assert result["title"] == "Test"
    assert result["owner"] == "Jane"
    assert result["cards"] == []

def test_to_dict_missing_title():
    test_data = Board(board_id=1,
                      owner="Jane")
    
    result = test_data.to_dict()
    
    assert len(result) == 4
    assert result["board_id"] == 1
    assert result["title"] is None
    assert result["owner"] == "Jane"
    assert result["cards"] == []

def test_to_dict_missing_owner():
    test_data = Board(board_id=1,
                      title="Test")
    
    result = test_data.to_dict()
    
    assert len(result) == 4
    assert result["board_id"] == 1
    assert result["title"] == "Test"
    assert result["owner"] is None
    assert result["cards"] == []

def test_from_json_returns_board():
    test_data = {
                "title": "Test",
                "owner": "Jane"
                }
    
    result = Board.from_json(test_data)

    assert result.title == "Test"
    assert result.owner == "Jane"

def test_from_json_missing_title():
    test_data = {
            "owner": "Jane"
            }
    
    with pytest.raises(KeyError):
        result = Board.from_json(test_data)

def test_from_json_missing_owner():
    test_data = {
            "title": "Test"
            }
    
    with pytest.raises(KeyError):
        result = Board.from_json(test_data)

# Card model tests
def test_card_to_dict_no_missing_data():
    test_data = Card(card_id=1,
                    message="Test",
                    likes_count=0,
                    board_id=1)
    
    result = test_data.to_dict()

    assert len(result) == 4
    assert result["card_id"] == 1
    assert result["message"] == "Test"
    assert result["likes_count"] == 0
    assert result["board_id"] == 1

def test_card_to_dict_missing_message():
    test_data = Card(card_id=1,
                    likes_count=0,
                    board_id=1)
    
    result = test_data.to_dict()
    
    assert len(result) == 4
    assert result["card_id"] == 1
    assert result["message"] is None
    assert result["likes_count"] == 0
    assert result["board_id"] == 1

def test_from_json_returns_card():
    test_data = {"message": "Test"}
    
    result = Card.from_json(test_data)

    assert result.message == "Test"

def test_card_from_json_missing_message():
    test_data = {}
    
    with pytest.raises(KeyError):
        result = Card.from_json(test_data)