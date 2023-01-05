import pytest
from app.models.board import Board


# @pytest.mark.skip
def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# @pytest.mark.skip
def test_get_boards_one_saved_board(client):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "board_id": 1,
            "name": "New Year",
            "owner": "Ada"
        }
    ]


# @pytest.mark.skip
def test_get_board_not_found(client):
    # Act
    response = client.get("/boards/345")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Board 345 not found"}


@pytest.mark.skip
def test_delete_board(client, one_task):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "message" in response_body
    assert response_body == {
        "message": "Board #1 was deleted"
    }
    assert Board.query.get(1) == None


# @pytest.mark.skip
def test_delete_board_not_found(client):
    # Act
    response = client.delete("/boards/123")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {
                                "message" : "Board 123 not found"
                            }
    assert Board.query.all() == []


