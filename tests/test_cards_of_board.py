import pytest
from app.models.card import Card
from app.models.board import Board

#@pytest.mark.skip(reason="No way to test this feature yet")
def test_post_card_ids_to_board(client, one_board, three_cards):
    # Act
    response = client.post("/boards/1/cards", json={
        "cards_ids": [1, 2, 3]
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "id" in response_body
    assert "cards_ids" in response_body
    assert response_body == {
        "id": 1,
        "cards_ids": [1, 2, 3]
    }

    # Check that Goal was updated in the db
    assert len(Board.query.get(1).cards) == 3