"""Define the SQLAlchemy data model and tables."""
from typing import List

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship


class Base(DeclarativeBase):
    pass


class Message(Base):
    __tablename__ = "messages"

    id = sa.Column("id", sa.Integer, primary_key=True)
    content = sa.Column("content", sa.String)
    annotations: Mapped[List["Annotation"]] = relationship(
        back_populates="message", cascade="delete-orphan"
    )


class Code(Base):
    __tablename__ = "codes"

    id = sa.Column("id", sa.Integer, primary_key=True)
    code = sa.Column("code", sa.String, unique=True)
    annotations: Mapped[List["Annotation"]] = relationship(cascade="delete-orphan")


class Annotation(Base):
    __tablename__ = "annotations"

    id = sa.Column("id", sa.Integer, primary_key=True)
    message_id = sa.Column("message_id", sa.Integer, sa.ForeignKey("messages.id"))
    code_id = sa.Column("code_id", sa.Integer, sa.ForeignKey("codes.id"))
    start_idx = sa.Column("start_idx", sa.Integer)
    end_idx = sa.Column("end_idx", sa.Integer)
    message: Mapped["Message"] = relationship(back_populates="annotations")
    code: Mapped["Code"] = relationship(back_populates="annotations")
