from werkzeug.exceptions import HTTPException
from app.board_routes import validate_model
from app.models.board import Board
import pytest

def test_get_all_boards_with_no_records(client):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_boards_with_two_records(client, saved_user, two_saved_boards):
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
    assert "date_created" in response_body[1].keys()
    assert response_body[1]["id"] == 2
    assert response_body[1]["title"] == "Underwater Clown Board"
    assert response_body[1]["owner"] == "Test"
    assert response_body[1]["num_cards"] == 0
    assert response_body[1]["visible"] == True

# maybe delete this one? it feels irrelevant to our routes
def test_get_all_boards_with_title_query_matching_none(client, two_saved_boards):
    data = {"title": "Onomatopoeia"}
    response = client.get("/boards", query_string = data)
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

# maybe delete this one? it feels irrelevant to our routes
def test_get_all_boards_with_title_query_matching_one(client, two_saved_boards):
    data = {"title": "Hackspiration Board"}
    response = client.get("/boards", query_string = data)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0] == {
        "id": 1,
        "title": "Hackspiration Board",
        "owner": "Spaghetti"
    }

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
    assert response_body == {
        "id": 1,
        "title": "Hackspiration Board",
        "owner": "Test"
    }

def test_create_one_board(client, user):
    response = client.post("/boards", json = {
        "title": "Itsa Me, Chris Pratt",
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == ""

def test_delete_board(client, two_saved_boards):
    response = client.delete("/2")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {"message": "Board #2 successfully deleted"}