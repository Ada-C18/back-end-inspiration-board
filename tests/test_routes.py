import pytest
from app.models.board import Board


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


#@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_one_saved_board(client, one_board):
    # Act
    response = client.get("boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Our inspo board",
            "owner": "JJ"
        }
    ]