"""Provide CRUD operations on the database."""

from typing import Any, List

from sqlalchemy import delete, func, select, update
from sqlalchemy.orm import Session

from . import schemas as sch
from .models import Message


def count_messages(session: Session) -> int:
    """Count the number of messages in the database.

    Taken from: https://stackoverflow.com/questions/65754023/what-is-the-equivalent-of-query-count-in-the-sqlalchemy-1-4-orm  # noqa
    """
    result = session.execute(select(func.count(Message.id)))
    return int(result.scalar_one())


def create_message(session: Session, new_message: sch.CreateMessage) -> Message:
    message = Message(content=new_message.content)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def read_messages(session: Session) -> List[Any]:
    result = session.scalars(select(Message)).all()
    return list(result)


def update_message(session: Session, message: sch.UpdateMessage) -> None:
    statement = (
        update(Message).where(Message.id == message.id).values(content=message.content)
    )
    session.execute(statement)
    session.commit()


def delete_message(session: Session, message: sch.DeleteItem) -> None:
    statement = delete(Message).where(Message.id == message.id)
    session.execute(statement)
    session.commit()
