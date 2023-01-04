import pytest
from app.models.board import Board

# test get routes
#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_routes_returns_empty_list(client):
    
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_boards_one_saved_board(client, one_board):
    
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [{
        'id': 1,
        'title': 'Get Healthy',
        'owner': 'Isabella'
    }]

def test_get_specific_board(client, one_board):

    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "board" in response_body
    assert response_body == {
        "board" : {
            "id": 1,
            "title": "Get Healthy",
            "owner": "Isabella"
        }
    }