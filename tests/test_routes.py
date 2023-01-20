from app.models.card import Card
from app.models.board import Board
import pytest

#################### CARDS ####################
def test_get_card(client, one_card):
  # ACT
  response = client.get("/cards/1")
  response_body = response.get_json()

  # ASSERT
  assert response.status_code == 200
  assert "card" in response_body
  assert response_body == {"card": {"card_id":1, "message": "It's Friday!", "likes_count": 0}}

def test_get_card_not_found(client):
  # ACT
  response = client.get("/cards/1")
  response_body = response.get_json()

  # ASSERT
  assert response.status_code == 404
  assert response_body == {"msg": "Could not find model with id: 1"}

def test_create_card(client):
  # ACT
  response = client.post('/cards', json={"message":"It's Monday!"})
  response_body = response.get_json()

  # ASSERT
  assert response.status_code == 201
  assert response_body == {"card": {"card_id":1, "message": "It's Monday!", "likes_count": 0}}

def test_delete_card(client, one_card):
  # ACT
  response = client.delete("/cards/1")
  response_body = response.get_json()

  # ASSERT
  assert response.status_code == 200
  assert response_body == {"msg": "card 'It's Friday!' deleted"}

def test_add_like_to_card(client, one_card):
  # ACT
  response = client.patch("/cards/1")
  response_body = response.get_json()

  # ASSERT
  assert response.status_code == 200
  assert response_body == {"msg": f"card updated to 1 likes"}



#################### BOARDS ####################
def test_get_board(client, one_board):
  # ACT
  response = client.get("/boards/1")
  response_body = response.get_json()

  # ASSERT
  assert response.status_code == 200
  assert "board" in response_body
  assert response_body == {"board": {"board_id":1, "title": "Days of the Week", "owner": "Mike"}}

def test_get_board_not_found(client):
  # ACT
  response = client.get("/boards/1")
  response_body = response.get_json()

  # ASSERT
  assert response.status_code == 404
  assert response_body == {"msg": "Could not find model with id: 1"}


def test_create_board(client):
  # ACT
  response = client.post('/boards', json={"title":"Winter Activities","owner":"Melissa"})
  response_body = response.get_json()

  # ASSERT
  assert response.status_code == 201
  assert response_body == {"board": {"board_id":1, "title":"Winter Activities","owner":"Melissa"}}


def test_delete_board(client, one_board):
  # ACT
  response = client.delete("/boards/1")
  response_body = response.get_json()

  # ASSERT
  assert response.status_code == 200
  assert response_body == {"msg": "board 1 'Days of the Week' deleted"}

def test_a_card_belong_to_a_board(client, one_card_belongs_to_one_board, another_card):
  # ACT
  response = client.patch("/boards/1/card", json={"card_id": 2})
  response_body = response.get_json()

  # ASSERT
  assert response.status_code == 200
  assert response_body == {
    "board": {
        "board_id": 1,
        "cards": [
            {
                "board_id": 1,
                "card_id": 1,
                "likes_count": 0,
                "message": "It's Friday!"
            },
            {
                "board_id": 1,
                "card_id": 2,
                "likes_count": 0,
                "message": "It's Saturday!"
            }
        ],
        "owner": "Mike",
        "title": "Days of the Week"
    }
}





