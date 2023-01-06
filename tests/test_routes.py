import pytest
from app.models.card import Card
from app.models.board import Board


def test_create_board(client):
    # Act
    response = client.post(
        "/board",
        json={
            "title": "Inspirational Quotes",
            "owner": "Cristal",
        },
    )

    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board": {
            "id": 1,
            "title": "Inspirational Quotes",
            "owner": "Cristal",
        }
    }


def test_duplicate_board_returns_400(client):
    # Act
    response = client.post(
        "/board",
        json={
            "title": "Inspirational Quotes",
            "owner": "Cristal",
        },
    )
    duplicate_response = client.post(
        "/board",
        json={
            "title": "Inspirational Quotes",
            "owner": "Cristal",
        },
    )
    response_body = duplicate_response.get_json()

    # Assert
    assert duplicate_response.status_code == 400
