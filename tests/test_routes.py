from app.models.board import Board
from app.models.card import Card
import pytest

def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_boards_one_saved_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "We are all winners",
            "owner": "Team SWAM",
        }
    ]

def test_get_one_board_all_cards(client, one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 4
    assert response_body == {
            "id": 1,
            "title": "We are all winners",
            "owner": "Team SWAM",
            "cards": [
                {
                    "id":1,
                    "message":"You are doing great",
                    "likes_count":0
                }
            ]
        }
    
    ##TEST FAILED
#     AssertionError: assert {'cards': [],... all winners'} == {'cards': [{'... all winners'}
# E         Omitting 3 identical items, use -vv to show
# E         Differing items:
# E         {'cards': []} != {'cards': [{'id': 1, 'likes_count': 0, 'message': 'You are doing great'}]}
# E         Use -v to get more diff