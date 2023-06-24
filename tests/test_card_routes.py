from app.models.card import Card
import pytest


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_cards_no_saved_cards(client):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_cards_one_saved_card(client, one_card):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1

    assert response_body == {
        "card": {
            "card_id": 1,
            "message": "You regret 100 percent of the chances you did not take",
            "likes_count": 0,
        }
    }


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_card(client, one_card):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "card" in response_body
    assert response_body == {
        "card": {
            "card_id": 1,
            "message": "You regret 100 percent of the chances you did not take",
            "likes_count": 0,
        }
    }


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_card_not_found(client):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message":"card 1 not found"}


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_update_card(client, one_card):
    # Act
    response = client.put("/cards/1", json={
        "message": "YOLO"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "card" in response_body
    assert response_body == {
        "card": {
            "card_id": 1,
            "message": "YOLO",
            "likes_count": 0
        }
    }
    card = Card.query.get(1)
    assert card.message == "YOLO"
    assert card.likes_count == 0
    
# @pytest.mark.skip(reason="No way to test this feature yet")
def test_update_card_not_found(client):
    # Act
    response = client.put("/cards/1", json={
        "message": "Updated Card Message",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "card 1 not found"}


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_card(client, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        'details': 'Card 1 "You regret 100 percent of the chances you did not take" successfully deleted'}
    assert Card.query.get(1) == None


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_card_not_found(client):
    # Act
    response = client.delete("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == None
    assert Card.query.all() == []

