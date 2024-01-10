from fastapi import FastAPI
from .routers import user, company, auth
from . import models
from .database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(company.router)
