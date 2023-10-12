"""Provide an API to allow access to the database."""
from typing import Generator, Optional

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
    """Provide a database session dependency to API endpoints."""
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
    """Create a new message in the database."""
    return crud.create_message(session, message)


@app.get("/messages/", response_model=list[sch.Message])
def read_messages(
    search: Optional[str] = None,
    limit: Optional[int] = None,
    offset: int = 0,
    sort_by: Optional[str] = None,
    sort_asc: bool = True,
    session: Session = session_dependency,
) -> list[models.Message]:
    """Read `limit` messages from the database starting from `offset` containing
    `search` ordered by column `sort_by` in direction `sort_asc`.
    """
    return crud.read_messages(
        session=session,
        search=search,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_asc=sort_asc,
    )


@app.post("/messages/update/")
def update_message(
    message: sch.UpdateMessage, session: Session = session_dependency
) -> None:
    """Update the content of a given message from the database."""
    crud.update_message(session, message)


@app.post("/messages/delete/")
def delete_message(
    message: sch.DeleteItem, session: Session = session_dependency
) -> None:
    """Delete a given message from the database."""
    crud.delete_message(session, message)


@app.get("/count/", response_model=int)
def read_count(session: Session = session_dependency) -> int:
    """Count the number of messages in the database."""
    return crud.count_messages(session)
