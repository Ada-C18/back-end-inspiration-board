from app.models.board import Board

def test_get_all_boards_with_empty_db_returns_empty_list(client):
    response = client.get("/board")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_boards_one_saved_board(client, one_board):
    response = client.get("/board")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [{
        "board_id": 1,
        "title": "Inspirational Quotes", 
        "owner": "Tasha",
        "cards": []
    }]

def test_get_board(client, one_board):
    response = client.get("/board/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "board_id": 1,
        "title": "Inspirational Quotes", 
        "owner": "Tasha",
        "cards": []
    }

def test_get_board_not_found(client):
    response = client.get("/board/1")
    response_body = response.get_json()
    
    assert response.status_code == 404
    assert response_body == {
        "message": "Board 1 not found"
    }

def test_add_one_board(client):
    response = client.post("/board", json = {
        "title": "Ada quotes",
        "owner": "Ada Lovelace"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {"message": "Successfully created new board with id = 1"}

def test_add_board_must_contain_title(client):
    response = client.post("/board", json={
        "owner": "Tasha"
    })
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {
        "message": "missing info"
    }
    assert Board.query.all() == []

def test_delete_one_board(client, one_board):
    response = client.delete("/board/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "message": "Successfully deleted board with id: 1"
    }
    assert Board.query.get(1) == None

def test_delete_board_not_found(client):
    response = client.delete("/board/1")
    response_body = response.get_json()
    
    assert response.status_code == 404
    assert response_body == {
        "message": "Board 1 not found"
    }

def test_post_one_card_belonging_to_a_board(client, one_board):
    response = client.post("board/1/card", json={
        "message": "It's a great day!"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "message": "Card It's a great day! belonging to Inspirational Quotes successfully added"
    }

def test_get_all_cards_belonging_to_one_board_one_card(client, one_card_belongs_to_one_board):
    response = client.get("board/1/card")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {
            "card_id": 1,
            "message": "Do your best",
            "likes_count": 0
        }
    ]
    
def test_get_all_cards_belonging_to_one_board_no_cards(client, one_board):
    response = client.get("board/1/card")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_cards_belonging_to_a_board_two_cards(client, two_cards_belongs_to_one_board):
    response = client.get("board/1/card")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [{
        "card_id": 1,
        "message": "We've got this",
        "likes_count": 0
    },{
        "card_id": 2,
        "message": "Practice makes perfect",
        "likes_count": 0
    }]



