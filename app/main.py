from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from .auth.router import AuthRouter
from .users.router import UsersRouter
from .company.router import CompanyRouter
from .time_entry.router import TimeEntryRouter
from .projects.router import ProjectsRouter

from . import models
from .projects import models as ProjectModels
from .database import engine

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
    "https://cvtm.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(engine)
ProjectModels.Base.metadata.create_all(engine)


app.include_router(AuthRouter)
app.include_router(UsersRouter)
app.include_router(CompanyRouter)
app.include_router(TimeEntryRouter)
app.include_router(ProjectsRouter)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(
        os.environ.get('PORT', 8000)), log_level="info")
