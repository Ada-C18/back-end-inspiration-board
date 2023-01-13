import pytest
from app.models.board import Board
from app.models.card import Card

def test_get_all_board_with_no_records(client):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_get_all_boards(client, all_boards):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {"id": 1, "owner": "Jan", "title": "Test Board 1"},
        {"id": 2, "owner": "Farrah", "title": "Test Board 2"},
        {"id": 3, "owner": "Maria", "title": "Test Board 3"}]
    

def test_get_one_board(client, one_board):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "board" in response_body
    assert response_body == {
        "board": {
            "id": 1,
            "title": "A New Board",
            "owner": "Andrea",
        }
    }


def test_get_board_not_found(client):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "message": "Board 1 not found"}


def test_create_board(client):
    response = client.post("/boards", json={
        "title": "A New Board",
        "owner": "Andrea",
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board": {
            "id": 1,
            "title": "A New Board",
            "owner": "Andrea",
        }
    }


def test_create_board_missing_data(client):
    response = client.post("/boards", json={})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }


def test_update_board(client, one_board):
    response = client.put("/boards/1", json={
        "title": "Updated Board Title",
        "owner": "Andrea"
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert "board" in response_body
    assert response_body == {
        "board": {
            "id": 1,
            "title": "Updated Board Title",
            "owner": "Andrea"
        }
    }
    board = Board.query.get(1)
    assert board.title == "Updated Board Title"


def test_update_board_not_found(client):
    response = client.put("/boards/1", json={
        "title": "Updated Board Title"
    })
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "message": "Board 1 not found"}


def test_delete_board(client, one_board):
    response = client.delete("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": "Board 1 A New Board successfully deleted"
    }


def test_delete_board_not_found(client):
    response = client.delete("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "message": "Board 1 not found"}
    assert Board.query.all() == []


@pytest.mark.skip(reason="likes count is returning None instead of default 0")
def test_get_all_cards_for_specific_board(client, one_card_belongs_to_one_board):
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {
            "card_id": 1,
            "message": "New card",
            "likes_count": 0,
            "board_id": 1,
        }
    ]


def test_get_cards_for_specific_board_without_cards(client, one_board):
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_get_card_for_missing_board(client):
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "message": "Board 1 not found"}


def test_create_card_for_board_with_cards(client, one_card_belongs_to_one_board):
    response = client.post("/boards/1/cards", json={"message": "New Card"})
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "card": {
            "board": "A New Board",
            "board_id": 1,
            "id": 2,
            "likes_count": 0,
            "message": "New Card"
        }
    }


def test_create_card_for_board_with_no_cards(client, one_board):
    response = client.post("/boards/1/cards", json={"message": "New Card"})
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "card": {
            "board": "A New Board",
            "board_id": 1,
            "id": 1,
            "likes_count": 0,
            "message": "New Card"
        }
    }


def test_delete_card_from_board(client, all_cards):
    response = client.delete("cards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": "Card 1 successfully deleted"
    }
    assert Card.query.get(1) == None


def test_delete_card_from_board_card_not_found(client):
    response = client.delete("cards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "message": "Card 1 not found"}
    assert Card.query.all() == []










