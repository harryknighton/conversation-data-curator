"""Define the SQLAlchemy data model and tables."""

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Message(Base):
    __tablename__ = "messages"

    id = sa.Column("id", sa.Integer, primary_key=True)
    content = sa.Column("content", sa.String)
