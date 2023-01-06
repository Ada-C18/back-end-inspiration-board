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
    # new_board = Board.query.get(1)
    # assert new_board
    # asser new_board.
