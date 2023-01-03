from app.models.card import Card
import pytest

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_tasks_no_saved_tasks(client):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_cards_one_saved_cards(client, one_task):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "message": "Have a good day!",
            "likes_count": 0,
            
        }
    ]


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_card(client):
    # Act
    response = client.post("/cards", json={
        "message": "A Brand New Card",
        "likes_count": 0,
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "card" in response_body
    assert response_body == {
        "card": {
            "id": 1,
            "message": "A Brand New Card",
            "likes_count": 0,
           
        }
    }
    new_card = Card.query.get(1)
    assert new_card
    assert new_card.message == "A Brand New Card"
    assert new_card.likes_count == 0
   

