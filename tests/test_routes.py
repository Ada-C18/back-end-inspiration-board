from app.models.board import Board
import pytest

def test_get_empty_board_list(client):
  #act
  response = client.get("/boards")
  response_body = response.get_json()

  #assert
  assert response.status_code == 200
  assert response_body == []

def test_get_boards_one_saved_board(client, one_board):
    #act
  response = client.get("/boards")
  response_body = response.get_json()

  #assert
  assert response.status_code == 200
  assert len(response_body) == 1
  assert response_body == [
    {
      "board_id": 1,
      "title": "I am a board",
      "owner": "rykaliva"
    }
  ]

def test_get_one_board(client, one_board):
  #act
  response = client.get("/boards/1")
  response_body = response.get_json()

  #assert
  assert response.status_code == 200
  assert response_body == {
      "board_id": 1,
      "title": "I am a board",
      "owner": "rykaliva"
    }

def test_get_board_not_found(client):
  #act
  response = client.get("/boards/1")
  response_body = response.get_json()

  #assert 
  assert response.status_code == 404
  assert response_body == {"message": "Board 1 not found"}

def test_create_board(client):
    #act
    response = client.post("/boards", json={
        "title": "I am a board",
        "owner": "rykaliva"
    })
    response_body = response.get_json()

    #assert
    assert response.status_code == 201
    assert response_body == "Board I am a board successfully created"

def test_update_board(client, one_board):
  #act
  response = client.put("/boards/1", json={
    "title": "Updated board title",
    "owner": "Serilla"})
  response_body = response.get_json()

  assert response_body == "Board has been updated"
  board = Board.query.get(1)
  assert board.title == "Updated board title"
  assert board.owner == "Serilla"

def test_delete_board(client, one_board):
  #act
  response = client.delete("/boards/1")
  response_body = response.get_json()

  #assert
  assert response.status_code == 200
  assert response_body == "Board 1 successfully deleted"
  assert Board.query.get(1) == None

def test_delete_board_not_found(client):
  #act
  response = client.delete("/boards/1")
  response_body = response.get_json()

  #assert 
  assert response.status_code == 404
  assert response_body == {"message": "Board 1 not found"}
  assert Board.query.all() == []
