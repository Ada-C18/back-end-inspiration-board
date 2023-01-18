from app.models.card import Card

def test_delete_one_card(client, one_card):
    response = client.delete("/card/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "message": "Successfully deleted card with id: 1"
    }

def test_delete_one_card_
    response = client.delete("/card/1")
    response_body = response.get_json()

def test_update_likes_for_one_card(client, one_card):
    response = client.patch("/card/1", json = {"likes_count": 2})
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "message": "Successfully updated the likes count for Card ID 1"
    }