from app.models.card import Card
from app.models.board import Board
import pytest

# ==================================================================
# BOARD ROUTES TESTS
# ==================================================================

# BOARD GET


def test_get_all_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_boards(client, create_four_boards):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {"board_id": 1, "owner": "Grumpy Cat", "title": "Cats"},
        {"board_id": 2, "owner": "Snoopy", "title": "Dogs"},
        {"board_id": 3, "owner": "Toucan", "title": "Birds"},
        {"board_id": 4, "owner": "Jumper", "title": "Rabbits"},
    ]


def test_get_one_board(client, create_one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "board": {"board_id": 1, "owner": "Grumpy Cat", "title": "Kitty Treats"}
    }


# BOARD-CARD GET


def test_get_all_cards_in_one_board(client, create_four_cards_associated_with_a_board):
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {"board_id": 1, "card_id": 1, "likes_count": 0, "message": "Message #1"},
        {"board_id": 1, "card_id": 2, "likes_count": 0, "message": "Card #2"},
        {"board_id": 1, "card_id": 3, "likes_count": 0, "message": "Hello World"},
        {"board_id": 1, "card_id": 4, "likes_count": 0, "message": "hello hello"},
    ]


def test_get_all_cards_in_one_board_with_no_cards(client, create_one_board):
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


# BOARD POST
def test_create_new_board(client):
    response = client.post("/boards", json={"title": "Best Quotes Ever", "owner": "Me"})
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {"board_id": 1, "owner": "Me", "title": "Best Quotes Ever"}
    new_board = Board.query.get(1)
    assert new_board
    assert new_board.owner == "Me"
    assert new_board.title == "Best Quotes Ever"


# BOARD DELETE
def test_delete_one_board(client, create_one_board):
    response = client.delete("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "message" in response_body
    assert response_body == {"message": "Board 1 Kitty Treats was deleted"}

    response = client.get("/boards/1")
    assert response.status_code == 404


def test_delete_one_board_doesnt_exist(client):
    response = client.delete("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Board 1 not found"}

    assert Board.query.all() == []


# BOARD UPDATE (PUT)


# ==================================================================
# CARD ROUTES TESTS
# ==================================================================

# CARD DELETE


def test_delete_one_card(client, create_one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert "message" in response_body
    assert response_body == {"message": "Card 1 successfully deleted"}
    response = client.get("/cards/1")
    assert response.status_code == 404


def test_delete_one_card_when_there_are_no_cards(client):
    response = client.delete("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Id 1 not found"}
    assert Card.query.all() == []


# CARD PATCH


def test_patch_one_card_likes_count(client, create_card_with_likes):
    # Act
    response = client.patch("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "board_id": 1,
        "card_id": 1,
        "likes_count": 31,
        "message": "testing testing 123",
    }
    new_likes_card = Card.query.get(1)
    assert new_likes_card.likes_count == 31


# CARD GET


def test_get_one_card_by_id(client, create_one_card):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "card": {
            "board_id": 1,
            "card_id": 1,
            "likes_count": 0,
            "message": "testing testing 123",
        }
    }


def test_get_one_card_doesnt_exist(client):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Id 1 not found"}


# CARD POST


def test_create_one_card_in_one_board(client, create_one_board):
    response = client.post(
        "/cards", json={"message": "this is a test card", "board_id": 1}
    )
    response_body = response.get_json()

    assert response.status_code == 201
    assert "card" in response_body
    assert response_body == {
        "card": {
            "board_id": 1,
            "card_id": 1,
            "likes_count": 0,
            "message": "this is a test card",
        }
    }
    new_card = Card.query.get(1)
    assert new_card
    assert new_card.message == "this is a test card"
    assert new_card.likes_count == 0


def test_try_to_create_one_card_without_board_id(client):
    response = client.post("/cards", json={"message": "this is a test card"})
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": "Invalid or incomplete card data"}
