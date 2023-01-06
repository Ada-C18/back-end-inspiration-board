from app.models.card import Card
import pytest

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_card(client, one_card):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "message" in response_body
    assert response_body ==  {
            
            "message": "Go on my daily walk" 
        }
  

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_card_not_found(client):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "message" not in response_body  


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_card(client, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "message" in response_body
    assert response_body == {
        "details": 'Card 1 "Go on my daily walk" successfully deleted'
    }
    assert Card.query.get(1) == None  


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_card_not_found(client):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert "message" not in response_body
    assert Card.query.all() == []
   

 #@pytest.mark.skip(reason="No way to test this feature yet")
def test_post_card_ids_to_board(client, one_board, three_cards):
    # Act
    response = client.post("/boards/1/cards", json={
        "cards": [1, 2, 3]
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "id" in response_body
    assert "cards" in response_body
    
    assert response_body == {
        "id": 1,
        "cards": [1, 2, 3]
    }

    



