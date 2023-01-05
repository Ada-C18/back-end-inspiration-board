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