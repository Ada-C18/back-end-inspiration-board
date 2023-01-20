from werkzeug.exceptions import HTTPException
from app.models.card import Card
from app.models.board import Board
import pytest

def test_delete_one_card(client, one_card_to_one_board):
    response = client.delete("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert Board.query.get(1).cards == []

def test_delete_card_not_found(client):
    response = client.delete("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Card 1 not found"}

def test_delete_card_invalid_id(client):
    response = client.delete("/cards/xxx")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": "Card xxx has an invalid id"}

def test_update_one_card_likes(client, one_card_to_one_board):
    # Act
    response = client.patch("/cards/1/like", json={
        "likes_count": 2
    })
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 200
    assert "card" in response_body
    assert response_body == {
        "card": {
            "card_id": 1,
            "message": "Test Message",
            "likes_count": 2
        }
    }
    
    card = Card.query.get(1)
    assert card.likes_count == 2

