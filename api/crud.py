from sqlmodel import select, Session

from .models import User, UserCreate, UserUpdate
from .security import get_password_hash, verify_password


def get_user_by_name(*, session: Session, name: str):
    statement = select(User).where(User.name == name)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, name: str, password: str):
    db_user = get_user_by_name(session=session, name=name)

    if not db_user:
        return None

    if not verify_password(password, db_user.hashed_password):
        return None

    return db_user


def get_users(*, session: Session, offset: int = 0, limit: int = 100):
    statement = select(User).offset(offset).limit(limit)
    all_users = session.exec(statement).all()
    return all_users


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={
            "hashed_password": get_password_hash(user_create.password)}
    )

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate):
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}

    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password

    db_user.sqlmodel_update(user_data, update=extra_data)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
