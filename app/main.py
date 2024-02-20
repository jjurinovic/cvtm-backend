from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .auth.router import AuthRouter
from .users.router import UsersRouter
from .company.router import CompanyRouter
from .time_entry.router import TimeEntryRouter
from . import models
from .database import engine

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)

app.include_router(AuthRouter)
app.include_router(UsersRouter)
app.include_router(CompanyRouter)
app.include_router(TimeEntryRouter)
