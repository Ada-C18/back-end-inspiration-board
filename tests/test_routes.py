from app.models.board import Board 
import pytest


def test_get_tasks_no_saved_tasks(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []