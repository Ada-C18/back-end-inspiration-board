import pytest
from app.models.card import Card
from app.models.board import Board


def test_create_board(client):
    # Act
    response = client.post(
        "/board",
        json={
            "title": "Inspirational Quotes",
            "owner": "Cristal",
        },
    )

    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "board" in response_body
    assert response_body == {
        "board": {
            "id": 1,
            "title": "Inspirational Quotes",
            "owner": "Cristal",
        }
    }


def test_duplicate_board_returns_400(client):
    # Act
    response = client.post(
        "/board",
        json={
            "title": "Inspirational Quotes",
            "owner": "Cristal",
        },
    )
    duplicate_response = client.post(
        "/board",
        json={
            "title": "Inspirational Quotes",
            "owner": "Cristal",
        },
    )
    response_body = duplicate_response.get_json()

    # Assert
    assert duplicate_response.status_code == 400


def test_read_all_boards(client, three_boards):
    # Act
    response = client.get("/board")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 1,
            "title": "Inspirational Quotes",
            "owner": "Cristal",
            # cards=[],
        },
        {
            "id": 2,
            "title": "To-do",
            "owner": "Annie",
            # cards=[],
        },
        {
            "id": 3,
            "title": "Thoughts",
            "owner": "Cristal",
            # cards=[],
        },
    ]


def test_read_one_board(client, one_board):
    # Act
    response = client.get("/board/Inspiration")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == {
        "board": {
            "id": 1,
            "title": "Inspiration",
            "owner": "Cristal",
            "cards": [
                {
                    "board_id": 1,
                    "id": 1,
                    "likes_count": 54,
                    "message": "does this return an int",
                },
                {
                    "board_id": 1,
                    "id": 2,
                    "likes_count": 0,
                    "message": "we're testing more",
                },
                {"board_id": 1, "id": 3, "likes_count": 17, "message": "lots of cards"},
                {
                    "board_id": 1,
                    "id": 4,
                    "likes_count": 20,
                    "message": "no sql databases",
                },
                {
                    "board_id": 1,
                    "id": 5,
                    "likes_count": 6,
                    "message": "no concept of migrations",
                },
            ],
        }
    }


# def test_read_one_board_invalid_title_returns_400(client):
#     pass
