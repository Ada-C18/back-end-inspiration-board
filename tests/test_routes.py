from app.models.card import Card
from app.models.board import Board
import pytest

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_card(client):
    response = client.post("/cards", json={
        "message": "test message"
    })
    response_body = response.get_json()
    assert response_body == {
        "card": {
            "card_id": 1,
            "message": "test message",
            "likes_count": 0
        }
    }
    new_card = Card.query.get(1)
    assert new_card
    assert new_card.message == "test message"

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_one_card(client, one_card):
    response = client.delete("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": "Card 1 'Go on my daily walk 🏞' successfully deleted"
    }
    assert Card.query.get(1) == None

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_board(client):
    response= client.post("/boards", json={
        "title": "workout",
        "owner": "bianca"
        })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board":{
            "board_id": 1,
            "title": "workout",
            "owner": "bianca"
    }
    }
def test_get_one_board(client, one_board):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
            "board_id": 1,
            "title": "workout",
            "owner": "bianca"
    }

def test_delete_one_board(client,one_board):
    response = client.delete("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "details": "Board 1 'workout' successfully deleted"
        }
    assert Board.query.get(1) == None

def test_add_card_to_board(client, one_board, one_card):
    response = client.post("/boards/1/cards", json={
        "card_id": 1
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert "board_id" in response_body
    assert response_body == {
        "board_id": 1,
        "cards": ['Go on my daily walk 🏞'
        ]
    }

def test_delete_card_from_board(client,one_board, one_card):
    new_card = client.post("/boards/1/cards", json={
        "card_id": 1
    })
    response = client.delete("/cards/1", json={
        "card_id": 1
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "details": "Card 1 'Go on my daily walk 🏞' successfully deleted"
    }