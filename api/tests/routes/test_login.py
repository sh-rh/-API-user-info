from fastapi.testclient import TestClient
from sqlmodel import Session, select

from api.security import verify_password
from api.models import User


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": 'admin',
        "password": 'q',
    }
    r = client.post("/token", data=login_data)

    tokens = r.json()

    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_incorrect_password(client: TestClient):
    login_data = {
        "username": 'admin',
        "password": "incorrect",
    }
    r = client.post('/token', data=login_data)

    assert r.status_code == 400


def test_use_access_token(client: TestClient, superuser_token: dict[str, str]):
    r = client.post(f"/test-token", headers=superuser_token)

    result = r.json()
    assert r.status_code == 200
    assert "name" in result
