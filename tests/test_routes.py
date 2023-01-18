from app.models.board import Board
import pytest

# test CREATE route
def test_create_board(client):
    # Act
    response = client.post("/board", json={
        "title": "a board for testing",
        "owner": "Turing",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {"board" : {
        "owner": "Turing",
        "title": "a board for testing"
    }}

    new_board = Board.query.get(1)
    assert new_board
    assert new_board.title == "a board for testing"
    assert new_board.owner == "Turing"

def test_create_without_owner(client):
    # Act
    response = client.post("/board", json={
        "title": "a board for testing",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"error message" : "Invalid data. Must include owner"}

# tests READ route
def test_get_all_boards(client, one_board):
    # Act
    response = client.get("/board")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [{
        "board_id": 1,
        "cards" : [],
        "owner": "Ada",
        "title": "A test board"
    }]

def test_get_one_board(client, one_board):
    # Act
    response = client.get("/board/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {"board":{
        "owner": "Ada",
        "title": "A test board"
    }}

def test_cant_get_board_out_of_range(client, one_board):
    # Act
    response = client.get("/board/100")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"error message":"Board 100 not found"}

# tests DELETE route
def test_delete_board(client, one_board):
    # Act
    response = client.delete("/board/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "message" in response_body
    assert response_body == {
        "message": "Board successfully deleted"
    }
    assert Board.query.get(1) == None