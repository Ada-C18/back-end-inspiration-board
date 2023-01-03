import pytest

# test get routes
@pytest.mark.skip(reason="No way to test this feature yet")
def test_get_routes_returns_empty_list(client):
    
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

