from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, func

from .. import crud

from ..models import User, UserCreate, UserPublic, UserUpdate, UsersPublic
from ..deps import CurrentUser, SessionDep, get_current_active_superuser

router = APIRouter()


@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser):
    return current_user


@router.get("/", dependencies=[Depends(get_current_active_superuser)], response_model=UsersPublic)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100):
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return UsersPublic(data=users, count=count)


@router.post("/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic)
def create_user(*, session: SessionDep, user_in: Annotated[UserCreate, Depends()]):
    user = crud.get_user_by_name(session=session, name=user_in.name)

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = crud.create_user(session=session, user_create=user_in)
    return user


@router.patch("/{user_id}", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic,)
def update_user(*, session: SessionDep, user_id: int, user_in:  Annotated[UserUpdate, Depends()]):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )

    if user_in.name:
        existing_user = crud.get_user_by_name(
            session=session, name=user_in.name)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this name already exists"
            )

    db_user = crud.update_user(
        session=session, db_user=db_user, user_in=user_in)
    return db_user


@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)])
def delete_user(session: SessionDep, current_user: CurrentUser, user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )

    session.delete(user)
    session.commit()
    return {'msg': "User deleted successfully"}
