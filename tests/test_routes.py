from werkzeug.exceptions import HTTPException
from app.board_routes import validate_model
from app.models.board import Board
from app.models.card import Card
import pytest

def test_get_all_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_boards_one_saved_boards(client, one_board):
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


def test_get_all_boards_four_saved_boards(client, four_boards):
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

def test_get_one_board_not_found(client):
    # Act
    response = client.get("boards/5")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "5 not found"}

def test_get_cards_from_one_board_no_saved_cards(client, one_board):
    # Act
    response = client.get("boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# @pytest.mark.skip
def test_get_cards_from_one_board(client,four_boards, one_card):
    # Act
    response = client.get("boards/3/cards")
    response_body = response.get_json()


    # Assert
    assert response.status_code == 200
    for response in response_body:
        assert "message" in response
        assert response["board_id"] == 3
    