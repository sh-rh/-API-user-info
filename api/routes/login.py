from datetime import timedelta
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, HTTPException

from .. import crud, security
from ..deps import CurrentUser, SessionDep
from ..models import Token, UserPublic

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


@router.post("/token")
def login_for_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = crud.authenticate(
        session=session, name=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = security.create_access_token(
        subject=user.id, expires_delta=access_token_expires)

    return Token(access_token=access_token)


@router.post("/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser):
    return current_user
