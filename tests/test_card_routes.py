from werkzeug.exceptions import HTTPException
from app.models.card import Card
import pytest


def test_delete_one_card(client):
    pass

def test_update_one_card_likes(client, one_card): # Thao
    # Act
    response = client.put("/cards/1/like", json={
        "message": "Test Message",
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

