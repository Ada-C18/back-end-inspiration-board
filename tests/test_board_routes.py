from werkzeug.exceptions import HTTPException
from app.models.board import Board
import pytest


def test_get_all_boards_with_no_records(client):
    pass

def test_get_all_boards_with_three_records(client, three_boards):
    pass

def test_get_one_board_with_invalid_id(client, three_boards):
    # Act
    response = client.get("/boards/xxx")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Board xxx has an invalid id"}

def test_get_one_board_with_wrong_id(client, three_boards):
    # Act
    response = client.get("/boards/5")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Board 5 not found"}

def test_get_one_board(client, three_boards):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "board" in response_body
    assert response_body == {
        "board": {
            "id": 1,
            "title": "Reminders",
            "owner": "Thao"
        }
    }

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
    # Act
    response = client.post("/boards", json={
        "owner": "Test Owner"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid Data"
    }
    assert Board.query.all() == []


def test_create_one_board_no_owner(client):   # THAO
    # Act
    response = client.post("/boards", json={
        "title": "A Brand New Board"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid Data"
    }
    assert Board.query.all() == []

    