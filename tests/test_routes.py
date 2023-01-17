from werkzeug.exceptions import HTTPException
from app.board_routes import validate_model
from app.models.board import Board
from app.models.card import Card
import pytest

def test_get_all_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_boards_one_saved_boards(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "test board 1",
            "owner": "QP/Lin"
        }
    ]


def test_get_all_boards_four_saved_boards(client, four_boards):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 4
    assert response_body == [
        {
            "id": 1,
            "title": "test board 1",
            "owner": "QP/Lin"
        },
        {
            "id": 2,
            "title": "test board 2",
            "owner": "QP/Lin"
        },
        {
            "id": 3,
            "title": "test board 3",
            "owner": "QP/Lin"
        },
        {
            "id": 4,
            "title": "test board 4",
            "owner": "QP/Lin"
        }
    ]

def test_get_specific_board(client, four_boards):
    # Act
    response = client.get("boards/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "title" in response_body
    assert response_body == {
        "id": 3,
        "title": "test board 3",
        "owner": "QP/Lin"
    }

def test_get_one_board_not_found(client):
    # Act
    response = client.get("boards/5")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "5 not found"}
    

def test_create_board(client):
    #Act
    response = client.post("/boards", json={
        "title": "A New Board",
        "owner": "Lin/QP"
    })

    response_body = response.get_json()

    #Assert
    assert response.status_code == 201
    new_board = Board.query.get(1)
    assert new_board
    assert new_board.title == "A New Board"
    assert new_board.owner == "Lin/QP"


def test_delete_board(client, one_board):
    #Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response_body == {"details": 'Board 1 successfully deleted'}
    assert Board.query.get(1) == None
    
# @pytest.mark.skip
def test_delete_board_not_found(client):
    #Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 404
    assert response_body == {
        "message" : "1 not found"
    }
    assert  Board.query.all() == []


def test_get_cards_from_one_board_no_saved_cards(client, one_board):
    # Act
    response = client.get("boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_cards_from_one_board(client,four_boards, one_card):
    # Act
    response = client.get("boards/3/cards")
    response_body = response.get_json()


    # Assert
    assert response.status_code == 200
    for response in response_body:
        assert "message" in response
        assert response["board_id"] == 3

# @pytest.mark.skip
def test_create_card(client, four_boards, one_card):
    #Act
    response = client.post("boards/3/cards", json={
        "message": "A New Card for Board 3",
        "likes_count": 0,
        "board_id": 3
    })

    response_body = response.get_json()

    #Assert
    assert response.status_code == 201
    new_card = Card.query.get(1)
    assert new_card
    assert new_card.message == "A New Card for Board 3"
    assert new_card.likes_count == 0
    assert new_card.board_id == 3


def test_update_card(client, four_boards, one_card):
    #Act
    response = client.put("cards/1/like", json={
        "message": "A New Card for Board 3",
        "likes_count": 0 
    })

    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    # assert response_body["likes_count"] == 1


def test_delete_card(client, one_card_belongs_to_one_board):
    #Act
    response = client.delete("cards/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    response_body == {"details": "Card 1 successfully deleted"}
    assert Card.query.get(1) == None

