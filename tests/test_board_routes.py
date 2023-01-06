import pytest
from app.models.board import Board

# test get routes
#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_routes_returns_empty_list(client):
    
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_boards_one_saved_board(client, one_card_belongs_to_one_board):
    
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [{
        'board_id': 1,
        'title': 'Get Healthy',
        'owner': 'Isabella',
        'cards': [{
                
                'card_id': 1, 
                'likes_count': 0, 
                'message': "You've got this!"}]
    }]

def test_get_specific_board(client, one_board):

    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "board" in response_body
    assert response_body == {
        "board" : {
            "board_id": 1,
            "title": "Get Healthy",
            "owner": "Isabella",
            "cards": []
        }
    }
def test_get_board_not_found(client):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {'message': "Board 1 was not found"}


def test_create_board(client):
    response = client.post("/boards", json={
        "title": "Atomic Habits",
        "owner": "Presley",
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board": {
            "board_id": 1,
            "title": "Atomic Habits",
            "owner": "Presley"
        }
    }

    new_board = Board.query.get(1)

    assert new_board
    assert new_board.title == "Atomic Habits"
    assert new_board.owner == "Presley"


def test_create_board_must_contain_title(client):
    # Act
    response = client.post("/boards", json={
        "owner": "Test"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Board.query.all() == []

def test_create_board_must_contain_owner(client):
    # Act
    response = client.post("/boards", json={
        "title": "A Brand New Board"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Board.query.all() == []

def test_delete_board(client, one_board):
    response = client.delete("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Board 1 "Get Healthy" successfully deleted'
    }
    assert Board.query.get(1) == None