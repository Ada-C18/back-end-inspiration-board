from app.models.board import Board
import pytest



# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get('/boards')
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_boards_one_saved_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "board_id": 1,
            "title": "Testing board 1",
            "owner": "VTV"
        }
    ]


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_board(client, one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
            "board_id": 1,
            "title": "Testing board 1",
            "owner": "VTV"
        }

# @pytest.mark.skip(reason="test to be completed by student")
def test_get_board_not_found(client):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body["msg"] == "Could not find Board item with id: 1"
   


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "My New Board",
        "owner": "Chetahs"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {   
            "board_id": 1,
            "title": "My New Board",
            "owner": "Chetahs"   
    }


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_board_must_contain_title(client):
    # Act
    response = client.post("/boards", json={
        "owner": "Tester"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert Board.query.all() == []


# @pytest.mark.skip(reason="No way to test this feature yet")
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

