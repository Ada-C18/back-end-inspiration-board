import pytest
from app.models.card import Card

# test GET routes

def test_get_cards_returns_empty_list(client):
    
    response = client.get("/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_cards_one_saved_card(client, one_card):
    response = client.get("/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1