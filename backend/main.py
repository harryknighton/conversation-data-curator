"""Create an API to allow access to the database."""
from typing import Generator

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


session_dependency = Depends(get_session)


@app.get("/test/")
def create_test_messages(session: Session = session_dependency) -> None:
    crud.create_test_messages(session)


@app.get("/messages/", response_model=list[schemas.Message])
def read_messages(session: Session = session_dependency) -> list[models.Message]:
    return crud.read_messages(session)


@app.get("/count/", response_model=int)
def read_count(session: Session = session_dependency) -> int:
    return crud.count_messages(session)
