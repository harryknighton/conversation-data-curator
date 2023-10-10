"""Provide CRUD operations on the database."""

from typing import Any, List

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.models import Message


def count_messages(session: Session) -> int:
    """Count the number of messages in the database.

    Taken from: https://stackoverflow.com/questions/65754023/what-is-the-equivalent-of-query-count-in-the-sqlalchemy-1-4-orm  # noqa
    """
    result = session.execute(select(func.count(Message.id)))
    return int(result.scalar_one())


def create_test_messages(session: Session) -> None:
    create_message(session, content="What's on your mind?")
    create_message(session, content="I'm so scared for tonight")


def create_message(session: Session, content: str) -> Message:
    message = Message(content=content)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def read_messages(session: Session) -> List[Any]:
    result = session.scalars(select(Message)).all()
    return list(result)  # list() needed for type hinting
