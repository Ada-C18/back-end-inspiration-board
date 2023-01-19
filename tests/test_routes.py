from werkzeug.exceptions import HTTPException
from app.board_routes import validate_model
from app.models.board import Board
from app.models.user import User
import pytest

def test_get_all_boards_with_no_records(client):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_boards_with_two_records(client, two_saved_boards):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert "date_created" in response_body[0].keys()
    assert response_body[0]["id"] == 1
    assert response_body[0]["title"] == "Hackspiration Board"
    assert response_body[0]["owner"] == "Test"
    assert response_body[0]["num_cards"] == 0
    assert response_body[0]["visible"] == True
    assert response_body[0]["card_color"] == "black"
    assert "date_created" in response_body[1].keys()
    assert response_body[1]["id"] == 2
    assert response_body[1]["title"] == "Underwater Clown Board"
    assert response_body[1]["owner"] == "Test"
    assert response_body[1]["num_cards"] == 0
    assert response_body[1]["visible"] == True
    assert response_body[1]["card_color"] == "black"

def test_get_one_board_missing_record(client, two_saved_boards):
    response = client.get("/boards/3")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Board 3 not found"}

def test_get_one_board_invalid_id(client, two_saved_boards):
    response = client.get("/boards/pickle")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": "Board pickle invalid"}

def test_get_one_board(client, saved_user, two_saved_boards):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "date_created" in response_body.keys()
    assert response_body["id"] == 1
    assert response_body["title"] == "Hackspiration Board"
    assert response_body["owner"] == "Test"
    assert response_body["num_cards"] == 0
    assert response_body["visible"] == True
    assert response_body["card_color"] == "black"
    

def test_create_one_board(client, saved_user):
    response = client.post("/boards", json = {
        "title": "Itsa Me, Chris Pratt",
        "user_id": 1,
        "card_color": "periwinkle"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "date_created" in response_body.keys()
    assert response_body["id"] == 1
    assert response_body["title"] == "Itsa Me, Chris Pratt"
    assert response_body["owner"] == "Test"
    assert response_body["num_cards"] == 0
    assert response_body["visible"] == True
    assert response_body["card_color"] == "periwinkle"


def test_delete_board(client, two_saved_boards):
    response = client.delete("/2")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {"message": "Board #2 successfully deleted"}