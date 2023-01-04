from app.models.board import Board
from app.models.card import Card


def test_get_all_boards_no_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_boards_one_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "name": "Test Board",
            "owner": "Test Owner",
        }
    ]


def test_get_all_boards_one_board_three_cards(client, one_board_three_cards):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1,
            "name": "Test Board",
            "owner": "Test Owner",
        }
    ]
