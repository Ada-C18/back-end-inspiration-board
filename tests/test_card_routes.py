from werkzeug.exceptions import HTTPException
from app.models.card import Card
from app.models.board import Board
import pytest


def test_delete_one_card(client, one_card_to_one_board):
    response = client.delete("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert Board.query.get(1).cards == []