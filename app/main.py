from fastapi import FastAPI
from .routers import user, company, auth, day
from . import models
from .database import engine
from datetime import date

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(company.router)
app.include_router(day.router)
