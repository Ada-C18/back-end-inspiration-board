from app.models.card import Card
import pytest


def test_delete_one_card(client, one_card):
    response = client.delete("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Card 1 "Go on my daily walk 🏞" successfully deleted'
    }
    assert Card.query.get(1) == None

