import pytest
from app.models.card import Card
from app.models.board import Board

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_post_card_ids_to_board(client, one_board, one_card):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "Everybody"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "board_id" in response_body

    assert response_body == {
        "board_id":1,
        "message": "Everybody",

    }

    # Check that Goal was updated in the db
    assert len(Board.query.get(1).cards) == 1

def test_get_cards_for_specific_board(client, one_card_belongs_to_one_board):

    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "cards" in response_body
    assert len(response_body["cards"]) == 1
    assert response_body == {
        "board_id": 1,
        "title": "Get Healthy",
        "owner": "Isabella",
        "cards": [{
            "message" : "You've got this!",
            "likes_count": 0,
            "card_id": 1,
            "board_id":1
        }]
    }

