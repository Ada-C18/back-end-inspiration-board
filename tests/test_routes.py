from werkzeug.exceptions import HTTPException
from app.board_routes import validate_model
from app.models.board import Board
from app.models.card import Card
import pytest

def test_get_all_books_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_all_books_one_saved_boards(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "test board 1",
            "owner": "QP/Lin"
        }
    ]


def test_get_all_books_four_saved_boards(client, four_boards):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 4
    assert response_body == [
        {
            "id": 1,
            "title": "test board 1",
            "owner": "QP/Lin"
        },
        {
            "id": 2,
            "title": "test board 2",
            "owner": "QP/Lin"
        },
        {
            "id": 3,
            "title": "test board 3",
            "owner": "QP/Lin"
        },
        {
            "id": 4,
            "title": "test board 4",
            "owner": "QP/Lin"
        }
    ]

def test_get_specific_board(client, four_boards):
    # Act
    response = client.get("boards/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "title" in response_body
    assert response_body == {
        "id": 3,
        "title": "test board 3",
        "owner": "QP/Lin"
    }
