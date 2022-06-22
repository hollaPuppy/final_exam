from .api import app
import json
from fastapi.testclient import TestClient

client = TestClient(app)


# def test_admin_auth():
#     data = {"user_name": "Admin", "user_password": "AdminAdmin"}
#     response = client.get('/users/auth', json.dumps(data))
#     assert response.status_code == 200
#     assert response.json() == {"detail": "OK"}


def test_get_top_players():
    response = client.get('/users/top_players/achv')
    assert response.status_code == 200