import pytest
from app.models.board import Board

# <---- boards ---->
# <---- create ---->

#@pytest.mark.skip
def test_create_a_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "Our inspo board", 
        "owner": "JJ"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "Our inspo board", 
        "owner": "JJ",
        "cards": [] 
    }

#@pytest.mark.skip
def test_create_a_board_missing_attributes(client):
    # Act
    response = client.post("/boards", json={
        "title": "Our inspo board"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {'details':'Title and owner are required'}

# <---- read ---->

#@pytest.mark.skip
def test_get_all_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["boards"] == []

#@pytest.mark.skip
def test_get_all_boards_two_saved_board(client, two_boards):
    # Act
    response = client.get("boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body["boards"]) == 2
    assert response_body["boards"] == [
        {
            "id": 1,
            "title": "Our inspo board",
            "owner": "JJ",
            "cards": []
        },
        {
            "id": 2,
            "title": "Aspirations",
            "owner": "Team Serval",
            "cards": []
        }
    ]

# <---- delete ---->

#pytest.mark.skip
def test_delete_a_board(client, two_boards):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {"details":'Board #1 "Our inspo board" was successfully deleted'}


# <---- cards ---->
# <---- create ---->

#@pytest.mark.skip
def test_create_a_card(client, two_boards):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "This is a card"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "message": "This is a card",
        "likes_count": 0
    }
# read all cards from a board

# post a card to a board

# post a card missing attributes

# delete a card from a board
