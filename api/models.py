from datetime import date

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    name: str = Field(unique=True, index=True)
    current_salary: int | None = None
    promotion_date: date | None = None
    is_superuser: bool = False
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str


class UserPublic(SQLModel):
    id: int
    name: str
    current_salary: int | None = None
    promotion_date: date | None = None
    is_superuser: bool = False
    is_active: bool = True


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class UserUpdate(SQLModel):
    name: str = Field(unique=True, index=True)
    current_salary: int | None = None
    promotion_date: date | None = None
    is_superuser: bool = False
    is_active: bool = True


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None
