from .api import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_admin_auth():
    response = client.get(
        "/users/auth",
        json={"user_name": "Admin", "user_password": "AdminAdmin"},
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "OK"}
