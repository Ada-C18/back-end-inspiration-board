from werkzeug.exceptions import HTTPException
from app.models.board import Board
from app.models.card import Card
import pytest


def test_get_all_boards_with_no_records(client):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []
    assert Board.query.all() == []

def test_get_all_boards_with_three_records(client, three_boards):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "board_id": 1,
            "title": "Reminders",
            "owner": "Thao"
        },
        {
            "board_id": 2,
            "title": "Pick Me Up Quotes",
            "owner": "Masha"
        },
        {
            "board_id": 3,
            "title": "Inspiration",
            "owner": "Neema"
        }
    ]

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

def test_create_one_board(client):
    response = client.post("/boards", json={
        "title": "Star Wars Quotes",
        "owner": "Thao"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "title" in response_body["board"] and "owner" in response_body["board"]
    assert response_body == {
        "board": {
            "id": 1,
            "title": "Star Wars Quotes",
            "owner": "Thao"
        }
    }

def test_create_one_board_no_title(client):
    response = client.post("/boards", json={
        "owner": "Thao"
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid request; missing necessary field(s)"
    }

def test_create_one_board_no_owner(client):
    response = client.post("/boards", json={
        "title": "Star Wars Quotes"
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid request; missing necessary field(s)"
    }

def test_get_all_cards_for_board(client, one_card_to_one_board):
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body["cards"]) == 1
    assert response_body == {
        "id": 1,
        "title": "Reminders",
        "owner": "Thao",
        "cards": [
            {
                "board_id": 1,
                "id": 1,
                "likes_count": 0,
                "message": "Finish Inspiration Board"
            }
        ]
    }

def test_get_all_cards_for_invalid_board(client):
    response = client.get("/boards/xxx/cards")
    response_body = response.get_json()

    assert response.status_code == 400
    assert "message" in response_body
    assert response_body == {
        "message": "Board xxx has an invalid id"
    }

def test_get_all_cards_for_nonexistant_board(client):
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    assert response.status_code == 404
    assert "message" in response_body
    assert response_body == {
        "message": "Board 1 not found"
    }

def test_create_one_card_for_board(client, one_board):
    response = client.post("/boards/1/cards", json={
        "message": "Drink water",
        "likes_count": 0,
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "id" in response_body["card"] and response_body["card"]["id"] == 1
    assert "message" in response_body["card"] and response_body["card"]["message"] == "Drink water"
    assert "likes_count" in response_body["card"] and response_body["card"]["likes_count"] == 0
    assert len(Board.query.get(1).cards) == 1

def test_create_one_card_message_too_long(client, one_board):
    response = client.post("/boards/1/cards", json={
        "message": "This is a very long message meant to go wayyyyyyy over the 40 character limit",
        "likes_count": 0,
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details":"Invalid request; message over 40 characters"}

def test_create_one_card_empty_message(client, one_board):
    response = client.post("/boards/1/cards", json={
        "message": "",
        "likes_count": 0,
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details":"Invalid request; message field cannot be empty"}

def test_create_one_card_missing_message(client, one_board):
    response = client.post("/boards/1/cards", json={
        "likes_count": 0,
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"details":"Invalid request; message field missing"}