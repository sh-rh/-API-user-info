import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, delete, create_engine, StaticPool


from api import crud

from .. import models
from ..main import app
from ..models import User, UserCreate, UserUpdate
from ..db import init_db, engine


@pytest.fixture(scope="session", autouse=True)
def db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        init_db(session)
        yield session
        statement = delete(User)
        session.exec(statement)
        session.commit()


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token(client: TestClient):
    login_data = {
        "username": 'admin',
        "password": 'q',
    }
    r = client.post('/token', data=login_data)
    token = r.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session):
    name = 'testuser'
    password = 'secret'
    current_salary = 9999
    promotion_date = '2030-01-01'

    user = crud.get_user_by_name(session=db, name=name)
    if not user:
        user_in_create = UserCreate(
            name=name,
            password=password,
            current_salary=current_salary,
            promotion_date=promotion_date)

        user = crud.create_user(session=db, user_create=user_in_create)


    login_data = {
        "username": name,
        "password": password,
    }
    r = client.post('/token', data=login_data)
    print(f'{user=}')
    print(f'{r.json()=}')
    token = r.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
