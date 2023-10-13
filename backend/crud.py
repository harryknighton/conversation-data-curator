"""Provide CRUD operations on the database."""

from typing import Any, List, Optional

import sqlalchemy as sa
from sqlalchemy.orm import Session

from . import schemas as sch
from .exceptions import MessageNotFoundError
from .models import Annotation, Code, Message

# -----------------------------------------------------------------------
# Messages


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


def delete_message(session: Session, message: sch.DeleteMessage) -> None:
    statement = sa.delete(Message).where(Message.id == message.id)
    session.execute(statement)
    session.commit()


# -----------------------------------------------------------------------
# Codes


def count_codes(session: Session) -> int:
    result = session.execute(sa.select(sa.func.count(Code.id)))
    return int(result.scalar_one())


def create_code(session: Session, new_code: sch.CreateCode) -> Optional[Code]:
    parts = new_code.code.split("/")
    current_code_string = ""
    current_code = None
    for part in parts:
        if not part:
            continue  # Skip empty string if new_code.code starts with '/'
        current_code_string += "/" + part
        check_if_exists = sa.select(Code).where(Code.code == current_code_string)
        code = session.execute(check_if_exists).scalar_one_or_none()
        if not code:
            current_code = Code(code=current_code_string)
            session.add(current_code)
    session.commit()
    session.refresh(current_code)
    return current_code  # Return only the original


def read_codes(
    session: Session,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_asc: bool = True,
) -> List[Any]:
    statement = sa.select(Code)
    if search is not None:
        statement = statement.where(Code.code.contains(search))
    column = sort_by if sort_by is not None else "code"
    ordering: sa.UnaryExpression[Any] = (
        sa.asc(column) if sort_by is None or sort_asc else sa.desc(column)
    )
    statement = statement.order_by(ordering)
    result = session.scalars(statement).all()
    return list(result)


def update_code(session: Session, new_code: sch.UpdateCode) -> None:
    get_old_code = sa.select(Code).where(Code.id == new_code.id)
    old_code = session.execute(get_old_code).scalar_one()
    get_subcodes = sa.select(Code).where(Code.code.contains(old_code.code))
    subcodes = session.execute(get_subcodes).scalars()
    old_code_length = len(old_code.code)
    for subcode in subcodes:
        subcode.code = new_code.code + subcode.code[old_code_length:]  # type: ignore
    session.commit()


def delete_code(session: Session, code: sch.DeleteCode) -> None:
    statement = sa.delete(Code).where(Code.code.contains(code.code))
    session.execute(statement)
    session.commit()


# -----------------------------------------------------------------------
# Annotations


def create_annotation(
    session: Session, new_annotation: sch.CreateAnnotation
) -> Annotation:
    get_message = sa.select(Message).where(Message.id == new_annotation.message_id)
    message = session.execute(get_message).scalar_one_or_none()
    if message is None:
        raise MessageNotFoundError()
    annotation = Annotation(
        code_id=new_annotation.code_id,
        start_idx=new_annotation.start_idx,
        end_idx=new_annotation.end_idx,
        message=message,
    )
    session.add(annotation)
    message.annotations.append(annotation)
    session.commit()
    session.refresh(annotation)
    return annotation


def read_annotations(session: Session, message_id: int) -> List[sch.AnnotationResponse]:
    get_message = sa.select(Message).where(Message.id == message_id)
    message: Message | None = session.execute(get_message).scalar_one_or_none()
    if message is None:
        raise MessageNotFoundError()
    return [
        sch.AnnotationResponse(
            result=(
                sch.Annotation.model_validate(annotation),
                sch.Code.model_validate(annotation.code),
            )
        )
        for annotation in message.annotations
    ]


def delete_annotation(session: Session, annotation: sch.DeleteAnnotation) -> None:
    statement = sa.delete(Annotation).where(Annotation.id == annotation.id)
    session.execute(statement)
    session.commit()
