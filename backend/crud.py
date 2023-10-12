"""Provide CRUD operations on the database."""

from typing import Any, List, Optional

import sqlalchemy as sa
from sqlalchemy.orm import Session

from . import schemas as sch
from .models import Message


def count_messages(session: Session) -> int:
    result = session.execute(sa.select(sa.func.count(Message.id)))
    return int(result.scalar_one())


def create_message(session: Session, new_message: sch.CreateMessage) -> Message:
    message = Message(content=new_message.content)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def read_messages(
    session: Session,
    search: Optional[str] = None,
    limit: Optional[int] = None,
    offset: int = 0,
    sort_by: Optional[str] = None,
    sort_asc: bool = True,
) -> List[Any]:
    statement = sa.select(Message)
    if search is not None:
        statement = statement.where(Message.content.contains(search))
    statement = statement.limit(limit).offset(offset)
    if sort_by:
        statement = statement.order_by(
            sa.asc(sort_by) if sort_asc else sa.desc(sort_by)
        )
    result = session.scalars(statement).all()
    return list(result)


def update_message(session: Session, message: sch.UpdateMessage) -> None:
    statement = (
        sa.update(Message)
        .where(Message.id == message.id)
        .values(content=message.content)
    )
    session.execute(statement)
    session.commit()


def delete_message(session: Session, message: sch.DeleteItem) -> None:
    statement = sa.delete(Message).where(Message.id == message.id)
    session.execute(statement)
    session.commit()
