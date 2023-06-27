import pytest

### BOARD TESTS ###

def test_get_all_boards_with_two_records(client, two_boards):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2

def test_get_all_boards_with_no_records(client):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_board_id_out_of_range(client, two_boards):
    response = client.get("/boards/3")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == "Board 3 not found"

def test_get_board_id_invalid(client, two_boards):
    response = client.get("boards/cat")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == "Board cat invalid"

def test_get_one_board(client, two_boards):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == dict(
        board_id = 1,
        title = "Inspirational Quotes",
        owner = "Jamal",
        cards=[]
    )

def test_create_one_board(client):
    response = client.post("/boards", json={
        "title": "Pokemon Cards",
        "owner": "Sarah"
    })

    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == "Board Pokemon Cards successfully created"

def test_create_board_no_title(client):
    test_data = {"owner": "Sarah"}

    with pytest.raises(KeyError, match="title"):
        response = client.post("/boards", json=test_data)

def test_create_board_no_owner(client):
    test_data = {"title": "Pokemon Cards"}

    with pytest.raises(KeyError, match="owner"):
        response = client.post("/boards", json=test_data)

def test_create_board_extra_keys(client):
    test_data = {
        "title": "Things to do on vacation",
        "owner": "Jae-lin",
        "description": "A new board!",
        "another": "More stuff!"
    }

    response = client.post("/boards", json=test_data)
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == "Board Things to do on vacation successfully created"

def test_delete_one_board(client, two_boards):
    response = client.delete("/boards/2")
    response_body = response.get_json()

    remaining_boards_response = client.get("/boards")
    remaining_boards = remaining_boards_response.get_json()

    assert response.status_code == 200
    assert response_body == "Board #2 successfully deleted"

    assert remaining_boards_response.status_code == 200
    assert len(remaining_boards) == 1

### CARD TESTS ###

def test_read_cards_from_board(client, three_cards):
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2

def test_read_all_cards(client, three_cards):
    response = client.get("/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3

def test_add_card_to_board(client, two_boards):
    test_data = {"message": "Don't stop believing!"}
    response = client.post("/boards/1/cards", json=test_data)
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == dict(
        card_id = 1,
        message = "Don't stop believing!",
        board_id = 1,
        likes_count = 0
    )

def test_add_card_missing_message(client, two_boards):
    with pytest.raises(KeyError, match="message"):
        response = client.post("/boards/1/cards", json={})

def test_add_card_extra_keys(client, two_boards):
    test_data = {"message": "Jane Eyre", "author": "Charlotte Bronte", "genre": "Romance"}
    response = client.post("/boards/2/cards", json=test_data)
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == dict(
        card_id = 1,
        message="Jane Eyre",
        board_id = 2,
        likes_count = 0
    )

def test_add_card_invalid_message(client, two_boards):
    test_data = {"message": "Hello, I am a message exceeding forty characters in length!!!!"}
    response = client.post("/boards/1/cards", json=test_data)
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == "Card message cannot exceed 40 characters"

def test_add_likes_to_card(client, three_cards):
    response = client.put("/cards/2/add_like")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == dict(
        card_id = 2,
        message = "You can do it!",
        likes_count = 1,
        board_id = 1
    )

def test_delete_card(client, three_cards):
    response = client.delete("/cards/3")
    response_body = response.get_json()

    remaining_cards_response = client.get("/cards")
    remaining_cards = remaining_cards_response.get_json()

    assert response.status_code == 200
    assert response_body == "Card 3 deleted"

    assert remaining_cards_response.status_code == 200
    assert len(remaining_cards) == 2 