"""Provide an API to allow access to the database."""
from typing import Generator, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models
from . import schemas as sch
from .database import SessionLocal, engine
from .exceptions import MessageNotFoundError

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


# -----------------------------------------------------------------------
# Messages


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


@app.post("/messages/create/", response_model=sch.Message)
def create_message(
    message: sch.CreateMessage, session: Session = session_dependency
) -> models.Message:
    """Create a new message in the database."""
    return crud.create_message(session, message)


@app.post("/messages/update/")
def update_message(
    message: sch.UpdateMessage, session: Session = session_dependency
) -> None:
    """Update the content of a given message from the database."""
    crud.update_message(session, message)


@app.post("/messages/delete/")
def delete_message(
    message: sch.DeleteMessage, session: Session = session_dependency
) -> None:
    """Delete a given message from the database."""
    crud.delete_message(session, message)


@app.get("/messages/count/", response_model=int)
def count_messages(session: Session = session_dependency) -> int:
    """Count the number of messages in the database."""
    return crud.count_messages(session)


# -----------------------------------------------------------------------
# Codes


@app.get("/codes/", response_model=list[sch.Code])
def read_codes(
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_asc: bool = True,
    session: Session = session_dependency,
) -> list[models.Code]:
    """Read codes from the database."""
    return crud.read_codes(
        session=session,
        search=search,
        sort_by=sort_by,
        sort_asc=sort_asc,
    )


@app.post("/codes/create/", response_model=Optional[sch.Code])
def create_code(
    code: sch.CreateCode, session: Session = session_dependency
) -> Optional[models.Code]:
    """Create a new code in the database if it does not already exist."""
    return crud.create_code(session, code)


@app.post("/codes/update/")
def update_code(code: sch.UpdateCode, session: Session = session_dependency) -> None:
    """Update a code in the database."""
    crud.update_code(session, code)


@app.post("/codes/delete/")
def delete_code(code: sch.DeleteCode, session: Session = session_dependency) -> None:
    """Delete a given code from the database."""
    crud.delete_code(session, code)


@app.get("/codes/count/", response_model=int)
def count_codes(session: Session = session_dependency) -> int:
    """Count the number of codes in the database."""
    return crud.count_codes(session)


# -----------------------------------------------------------------------
# Annotations


@app.get("/annotations/{message_id}/")
def read_annotations(
    message_id: int,
    session: Session = session_dependency,
) -> list[sch.AnnotationResponse]:
    """Read annotations from the database for a given message."""
    try:
        return crud.read_annotations(
            session=session,
            message_id=message_id,
        )
    except MessageNotFoundError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.post("/annotations/{message_id}/create/", response_model=sch.Annotation)
def create_annotation(
    annotation: sch.CreateAnnotation, session: Session = session_dependency
) -> models.Annotation:
    """Create a new annotation in the database for a given message."""
    try:
        return crud.create_annotation(session=session, new_annotation=annotation)
    except MessageNotFoundError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.post("/annotations/update/")
def update_annotation(
    annotation: sch.UpdateAnnotation, session: Session = session_dependency
) -> None:
    """Update the content of a given annotation from the database."""
    crud.update_annotation(session, annotation)


@app.post("/annotations/delete/")
def delete_annotation(
    annotation: sch.DeleteAnnotation, session: Session = session_dependency
) -> None:
    """Delete a given annotation from the database."""
    crud.delete_annotation(session, annotation)
