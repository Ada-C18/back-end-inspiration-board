from app.models.card import Card
import pytest


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_cards_no_saved_tasks(client):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_cards_one_saved_cards(client, one_card):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "card_id": 1,
            "message": "You got it!",
            "likes_count": 0,
            
        }
    ]

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_card(client):
    # Act
    response = client.post("/cards", json={
        "message": "A Brand New Card"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
            "card_id": 1,
            "message": "A Brand New Card",
            "likes_count": 0,
        }
    
    new_card = Card.query.get(1)
    assert new_card
    assert new_card.message == "A Brand New Card"
    assert new_card.likes_count == 0
   
#@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_card(client, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Card 1 "You got it!" successfully deleted' 
    }
    assert Card.query.get(1) == None
    

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_card_not_found(client):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404


    assert Card.query.all() == []
    assert "msg" in response_body
    assert response_body["msg"] == "Could not find card item with id: 1"
  

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_create_card_must_contain_message(client):
    # Act
    response = client.post("/cards", json={
        
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Card.query.all() == []



