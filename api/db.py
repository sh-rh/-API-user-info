from sqlmodel import Session, create_engine, select

from . import crud, models
from .models import User, UserCreate

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def init_db(session: Session):
    user = session.exec(select(User).where(User.name == 'admin')).first()

    if not user:
        user_in = UserCreate(
            name='admin',
            password='q',
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)
