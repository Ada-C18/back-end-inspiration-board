import unittest
from unittest.mock import Mock, patch
from app.models.board import Board
from app.models.card import Card
import pytest

def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_boards_one_saved_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "We are all winners",
            "owner": "Team SWAM",
        }
    ]

def test_get_one_board_all_cards(client, one_board, one_card):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 4
    print(response_body)
    assert response_body == {
            "id": 1,
            "title": "We are all winners",
            "owner": "Team SWAM",
            "cards": [
                {
                    "id":1,
                    "message":"You are doing great",
                    "likes_count":0
                }
            ]
        }

def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "A Brand New Board",
        "owner": "Test Owner",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board": {
            "id": 1,
            "title": "A Brand New Board",
            "owner": "Test Owner",
        }
    }
    new_board = Board.query.get(1)
    assert new_board
    assert new_board.title == "A Brand New Board"
    assert new_board.owner == "Test Owner"

def test_create_card(client, one_board):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "Test card message"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "card" in response_body
    assert response_body == {
        "card": {
            "id": 1,
            "likes_count": 0,
            "message": "Test card message",
        }
    }
    new_card = Card.query.get(1)
    assert new_card
    assert new_card.message == "Test card message"

def test_delete_card(client, one_board, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "Details" in response_body
    assert response_body == {
        "Details": "card 1 successfully deleted."
    }
    assert Card.query.get(1) == None

def test_delete_board(client, one_board):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "Details" in response_body
    # assert response_body == {
    #     'Details': "board 1 'We are all winners' successfully deleted."
    # }
    assert Board.query.get(1) == None

def test_mark_100_likes(client, one_board, one_card):
    # Arrange
    with patch("requests.post") as mock_get:
        mock_get.return_value.status_code = 200

    # Act
    response = client.patch("/cards/1/100")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "message" in response_body
    assert response_body == {
        "message": "Successfully updated Card ID `1`'s price to be 100"
    }
    assert Card.query.get(1).likes_count
