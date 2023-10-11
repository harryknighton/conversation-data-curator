"""Create an API to allow access to the database."""
from typing import Generator

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models
from . import schemas as sch
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Needed to allow same-origin CORS requests between the web app and API when run locally
# WARNING: This opens the app up to cross-site scripting attacks
# TODO: #17 Find a more secure method of allowing same origin requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


session_dependency = Depends(get_session)


@app.post("/messages/create/", response_model=sch.Message)
def create_message(
    message: sch.CreateMessage, session: Session = session_dependency
) -> models.Message:
    return crud.create_message(session, message)


@app.get("/test/")
def create_test_messages(session: Session = session_dependency) -> None:
    create_message(sch.CreateMessage(content="What's on your mind?"), session)
    create_message(sch.CreateMessage(content="I'm so scared for tonight"), session)


@app.get("/messages/", response_model=list[sch.Message])
def read_messages(session: Session = session_dependency) -> list[models.Message]:
    return crud.read_messages(session)


@app.post("/messages/update/")
def update_message(
    message: sch.UpdateMessage, session: Session = session_dependency
) -> None:
    crud.update_message(session, message)


@app.post("/messages/delete/")
def delete_message(
    message: sch.DeleteItem, session: Session = session_dependency
) -> None:
    crud.delete_message(session, message)


@app.get("/count/", response_model=int)
def read_count(session: Session = session_dependency) -> int:
    return crud.count_messages(session)
