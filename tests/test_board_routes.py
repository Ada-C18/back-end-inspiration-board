from app.models.board import Board
from app.models.card import Card


def test_get_all_board_with_no_records(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_boards_with_one_record(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "title": "This is an inspiration board",
            "owner": "Curious Georges",
            "board_id": 1
        }
    ]


def test_get_one_board(client, one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "board": {
            "title": "This is an inspiration board",
            "owner": "Curious Georges",
            "board_id": 1
        }
    }


def test_get_nonexistent_board(client):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"error": "Board 1 not found"}, 404


def test_get_all_cards_on_a_board(client, one_card_on_one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "board_id": 1,
        "cards": [{
            "card_id": 1,
            "board_id": 1,
            "message": "This is an inspirational card",
            "likes_count": 0
        }],
        "owner": "Curious Georges",
        "title": "This is an inspiration board"
    }


def test_all_cards_on_an_empty_board(client, one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "board_id": 1,
        "cards": [],
        "owner": "Curious Georges",
        "title": "This is an inspiration board"
    }


def test_get_all_cards_on_a_nonexistent_board(client):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"error": "Board 1 not found"}, 404


def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "My inspiration board",
        "owner": "Curious Georges"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "message": "Board 'My inspiration board' successfully created",
        "board": {
            "title": "My inspiration board",
            "owner": "Curious Georges",
            "board_id": 1
        }
    }
    new_board = Board.query.get(1)
    assert new_board
    assert new_board.title == "My inspiration board"
    assert new_board.owner == "Curious Georges"
    assert new_board.board_id == 1


def test_create_board_missing_body(client):
    # Act
    response = client.post("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "error": "Please include a request body with a title and owner"}


def test_create_board_missing_title(client):
    # Act
    response = client.post("/boards", json={
        "owner": "Curious Georges"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "error": "Please provide both the title and owner"}


def test_create_board_missing_owner(client):
    # Act
    response = client.post("/boards", json={
        "title": "My board"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "error": "Please provide both the title and owner"}


def test_delete_board(client, one_board):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "message": "Board 'This is an inspiration board' successfully deleted"}

    deleted_board_in_system = Board.query.get(1)
    assert not deleted_board_in_system


def test_delete_nonexistent_board(client):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"error": "Board 1 not found"}, 404


def test_delete_board_deletes_cards(client, one_card_on_one_board):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    deleted_board_in_system = Board.query.get(1)
    assert not deleted_board_in_system
    deleted_card_in_system = Card.query.get(1)
    assert not deleted_card_in_system
