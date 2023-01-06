from werkzeug.exceptions import HTTPException
from app.models.board import Board
from app.models.card import Card
import pytest


def test_get_all_boards_with_no_records(client):
    pass

def test_get_all_boards_with_three_records(client, three_boards):
    pass

def test_get_one_board_with_missing_record(client, three_boards):
    pass

def test_get_one_board(client, three_boards):
    pass

def test_create_one_board(client):
    pass

def test_create_one_board_no_title(client):
    pass

def test_create_one_board_no_owner(client):
    pass

def test_get_all_cards_for_board(client):
    pass

def test_get_all_cards_for_invalid_board(client):
    pass

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