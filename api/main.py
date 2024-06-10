from fastapi import FastAPI

from .routes import users, login
from .routes.lifespan import lifespan

app = FastAPI(lifespan=lifespan)


app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(login.router, tags=["login"])
