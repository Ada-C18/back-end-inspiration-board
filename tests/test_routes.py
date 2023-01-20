from app.models.card import Card
import pytest
from app.models.board import Board 

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_card(client, one_card):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "message" in response_body
    assert response_body ==  {
            
            "message": "You are doing great!" 
        }


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_card_not_found(client):
    # Act
    response = client.get("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Card 1 not found"} 

def test_get_card_invalid_url_peram(client):
    response = client.get("/cards/dog")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": "Card dog invalid" }

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_card(client, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Card 1 "You are doing great!" successfully deleted'
    }
    assert Card.query.get(1) == None  


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_card_not_found(client):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Card 1 not found"} 
    


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_post_card_ids_to_board(client, one_board, three_cards):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "You are doing great!"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "id" in response_body
    assert "message" in response_body
    
    assert response_body['message'] == "You are doing great!"

def test_card_list_for_board_with_cards(client, one_card_belongs_to_one_board):

    response = client.get("/boards/1/cards")
    response_body = response.get_json()
    messages = ["You are doing great!"]
    response_cards = [card["message"] for card in response_body['cards']]

    assert response.status_code == 200
    assert response_cards == messages
    assert len(response_cards) == 1
    

def test_get_cards_for_specific_board_no_board(client):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Board 1 not found"}

def test_get_cards_for_specific_board_no_cards(client, one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "cards" in response_body
    assert len(response_body["cards"]) == 0
    assert response_body == {
        "id": 1,
        "title": "January Board",
        "cards": [],
        "author": "r"
    }

def test_post_board(client):
    response = client.post("/boards", json={
        "author": "rk",
        "title": "new board 2"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "author" in response_body
    assert "title" in response_body
    
    assert response_body['title'] == "new board 2"
    assert response_body['author'] == "rk"

def test_get_one_board(client, one_board):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response_body == {'title':"January Board", 'author':"r", "id":1, "cards": []}
    assert response.status_code == 200