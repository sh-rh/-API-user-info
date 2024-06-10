from fastapi.testclient import TestClient
from sqlmodel import Session

from api import crud
from api.models import UserCreate
from api.tests.utils import random_string


def test_get_users_superuser_me(client: TestClient, superuser_token: dict[str, str]):
    r = client.get("users/me", headers=superuser_token)
    current_user = r.json()

    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["name"] == 'admin'


def test_get_users_normal_user_me(client: TestClient, normal_user_token_headers: dict[str, str]):
    r = client.get(f"users/me", headers=normal_user_token_headers)
    current_user = r.json()

    assert current_user
    assert current_user["name"] == 'testuser'
    assert current_user["current_salary"] == 9999
    assert current_user["promotion_date"] == '2030-01-01'


def test_create_user_by_normal_user(client: TestClient, normal_user_token_headers: dict[str, str]):
    username = 'testuser'
    password = 'secret'
    data = {"name": username, "password": password}
    r = client.post(
        f"/users/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 403


def test_retrieve_users(client: TestClient, superuser_token: dict[str, str], db: Session):
    username = random_string()
    password = random_string()
    user_in = UserCreate(name=username, password=password)
    crud.create_user(session=db, user_create=user_in)

    username2 = random_string()
    password2 = random_string()
    user_in2 = UserCreate(name=username2, password=password2)
    crud.create_user(session=db, user_create=user_in2)

    r = client.get(f"/users/", headers=superuser_token)
    all_users = r.json()

    assert len(all_users["data"]) > 1
    assert "count" in all_users
