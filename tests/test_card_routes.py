from app.models.board import Board
from app.models.card import Card


def test_get_all_cards_with_no_records(client):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_cards_with_one_record(client, one_card_on_one_board):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "card_id": 1,
            "board_id": 1,
            "message": "This is an inspirational card",
            "likes_count": 0
        }
    ]


def test_get_all_cards_from_multiple_boards(client, two_cards_on_two_boards):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert {
        "card_id": 1,
        "board_id": 1,
        "message": "This is an inspirational card",
        "likes_count": 0
    } in response_body
    assert {
        "card_id": 2,
        "board_id": 2,
        "message": "Hope you're having a great day!",
        "likes_count": 0
    } in response_body


def test_get_one_card(client, one_card_on_one_board):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "card": {
            "card_id": 1,
            "board_id": 1,
            "message": "This is an inspirational card",
            "likes_count": 0
        }
    }


def test_get_one_nonexistant_card(client):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"error": "Card 1 not found"}, 404


def test_create_card(client, one_board):
    # Act
    response = client.post("/cards", json={
        "message": "I feel inspired",
        "board_id": 1
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "message": "Card 'I feel inspired' successfully created",
        "Card": {
            "message": "I feel inspired",
            "board_id": 1,
            "card_id": 1,
            "likes_count": 0
        }
    }

    new_card = Card.query.get(1)
    this_board = Board.query.get(1)

    assert new_card.message == "I feel inspired"
    assert new_card.board_id == 1
    assert new_card.card_id == 1
    assert new_card.likes_count == 0

    assert this_board.cards == [new_card]


def test_create_card_missing_body(client, one_board):
    # Act
    response = client.post("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "error": "Please include a request body with a message and board id"}


def test_create_card_missing_board_id(client, one_board):
    # Act
    response = client.post("/cards", json={
        "message": "hello"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"error": "Please provide a message and board id"}


def test_create_card_missing_message(client, one_board):
    # Act
    response = client.post("/cards", json={
        "board_id": 1
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"error": "Please provide a message and board id"}


def test_create_card_with_likes_count(client, one_board):
    # Act
    response = client.post("/cards", json={
        "board_id": 1,
        "message": "hello",
        "likes_count": 5
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "message": "Card 'hello' successfully created",
        "Card": {
            "message": "hello",
            "board_id": 1,
            "card_id": 1,
            "likes_count": 0
        }}

    new_card = Card.query.get(1)
    this_board = Board.query.get(1)

    assert new_card.message == "hello"
    assert new_card.board_id == 1
    assert new_card.card_id == 1
    assert new_card.likes_count == 0

    assert this_board.cards == [new_card]


def test_create_card_on_nonexistent_board(client):
    # Act
    response = client.post("/cards", json={
        "board_id": 1,
        "message": "hello",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"error": "Board 1 not found"}, 404


def test_update_likes_on_card(client, one_card_on_one_board):
    # Act
    response = client.put("/cards/1", json={
        "likes_count": 5
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "message": "Likes count successfully updated",
        "card": {
            "card_id": 1,
            "board_id": 1,
            "message": "This is an inspirational card",
            "likes_count": 5
        }
    }

    this_card = Card.query.get(1)
    this_board = Board.query.get(1)
    assert this_card.likes_count == 5
    assert this_board.cards[0].likes_count == 5


def test_update_likes_on_card_missing_body(client, one_card_on_one_board):
    # Act
    response = client.put("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "error": "Please include a request body with a likes_count"}


def test_update_likes_on_card_missing_likes(client, one_card_on_one_board):
    # Act
    response = client.put("/cards/1", json={
        "likes": 5
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "error": "Please include a request body with a likes_count"}


def test_update_likes_on_nonexistent_card(client):
    # Act
    response = client.put("/cards/1", json={
        "likes": 5
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"error": "Card 1 not found"}


def test_delete_card(client, one_card_on_one_board):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {"message": "Card 1 successfully deleted"}

    deleted_card = Card.query.get(1)
    this_board = Board.query.get(1)
    assert not deleted_card
    assert not this_board.cards


def test_delete_nonexistent_card(client):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"error": "Card 1 not found"}
