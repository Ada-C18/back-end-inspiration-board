from werkzeug.exceptions import HTTPException
from app.models.board import Board
import pytest


def test_get_all_boards_with_no_records(client):
    pass

def test_get_all_boards_with_three_records(client, three_boards):
    pass

def test_get_one_board_with_missing_record(client, three_boards):
    pass

def test_get_one_board(client, three_boards):
    pass

def test_create_one_board(client): # Thao check nesting of response
    # Act
    response = client.post("/boards", json={
        "title": "A Brand New Board",
        "owner": "Test Owner",
    })
    response_body = response.get_json()
    
    #Assert
    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board": {
            "id": 1,
            "title": "A Brand New Board",
            "owner": "Test Owner"
        }
    }
    new_board = Board.query.get(1)
    assert new_board 
    assert new_board.title == "A Brand New Board"
    assert new_board.owner == "Test Owner"
    
def test_create_one_board_no_title(client):     # THAO
    pass

def test_create_one_board_no_owner(client):
    pass