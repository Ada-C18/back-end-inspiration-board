from app.models.card import Card
from app.models.board import Board
import pytest

def test_get_card(client, one_card):
  # ACT
  response = client.get("/cards/1")
  response_body = response.get_json()

  # ASSERT
  assert response.status_code == 200
  assert "card" in response_body
  assert response_body == {"card": {"card_id":1, "message": "It's Friday!"}}

