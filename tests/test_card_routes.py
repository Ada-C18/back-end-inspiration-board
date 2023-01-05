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
    assert response_body == [{
        "id": 1,
        "message": "You've got this!",
        "likes_count": 0
    }]

def test_get_specific_card(client, one_card):
    response = client.get("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "card" in response_body
    assert response_body == {
        "card": {
            "id": 1,
            "message": "You've got this!",
            "likes_count": 0
        }
    }

def test_get_card_not_found(client):
    response = client.get("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {'message': "Card 1 was not found"}

def test_create_card(client):
    response = client.post("/cards", json={
        "message": "You're a great friend :)"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "card" in response_body
    assert response_body == {
        "card": {
            "id": 1,
            "message": "You're a great friend :)",
            "likes_count": 0
        }
    }

    new_card = Card.query.get(1)

    assert new_card
    assert new_card.message == "You're a great friend :)"
