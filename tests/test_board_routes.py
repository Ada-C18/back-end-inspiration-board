from app.models.board import Board
import pytest


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_boards_one_saved_board(client, one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

# Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == {
            'owner': 'Sika',
            'title': 'Cool programming websites to checkout',
            'id': 1,
    }


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "Cool programming websites to checkout",
        "owner": "Sika"})
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 201
    assert "Cool programming websites to checkout" in response_body
    new_board = Board.query.first()
    assert new_board
    assert new_board.board_id == 1
    assert new_board.title == "Cool programming websites to checkout"
    assert new_board.owner == "Sika"


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_board_failed(client):
    response = client.post("/boards", json={})
    response_body = response.get_json()

    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": 'Invalid data'
    }
    assert Board.query.all() == []


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_board(client, one_board):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Board 1 "Cool programming websites to checkout" successfully deleted'
    } 
    assert Board.query.get(1) == None
    
    
# @pytest.mark.skip(reason="No way to test this feature yet")   
def test_delete_board_not_found(client):
    response = client.delete("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert Board.query.all() == []
    assert response_body == ''


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_cards_from_one_board(client, one_card_belongs_to_one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 200
    assert "cards" in response_body
    assert len(response_body["cards"]) == 1
    assert response_body == {
        "title": "Cool programming websites to checkout",
        "owner": "Sika",
        "cards": [
            {
                "card_id": 1,
                "message": "https:/dev.to",
                "likes_count": 0
            }
        ],
        "id": 1
    }


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_card_includes_board_id(client, one_card_belongs_to_one_board):
    response = client.get("/cards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "card" in response_body
    assert "board_id" in response_body["card"]
    assert response_body == {
        "card": {
            "card_id": 1,
            "board_id": 1,
            "message": "https:/dev.to",
            "likes_count": 0

        }
    }
