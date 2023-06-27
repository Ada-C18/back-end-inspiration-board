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

def test_create_book_extra_keys(client):
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

    assert response.status_code == 200
    assert response_body == "Board #2 successfully deleted"

### CARD TESTS ###

#TBD