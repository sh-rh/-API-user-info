from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from api import crud
from api.security import verify_password
from api.models import User, UserCreate, UserUpdate
from .utils import random_string




def test_create_user(db: Session):
    name = random_string()
    password = random_string()

    user_in = UserCreate(name=name, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    assert user.name == name
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Session):
    name = random_string()
    password = random_string()

    user_in = UserCreate(name=name, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    auth_user = crud.authenticate(session=db, name=name, password=password)

    assert auth_user
    assert user.name == auth_user.name


def test_not_authenticate_user(db: Session) -> None:
    name = random_string()
    password = random_string()
    user = crud.authenticate(session=db, name=name, password=password)
    assert user is None


def test_check_if_user_is_superuser(db: Session) -> None:
    name = random_string()
    password = random_string()

    user_in = UserCreate(name=name, password=password, is_superuser=True)
    user = crud.create_user(session=db, user_create=user_in)

    assert user.is_superuser is True
    

def test_get_user(db: Session) -> None:
    name = random_string()
    password = random_string()

    user_in = UserCreate(name=name, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    user_2 = db.get(User, user.id)

    assert user_2
    assert user.name == user_2.name
    assert jsonable_encoder(user) == jsonable_encoder(user_2)
