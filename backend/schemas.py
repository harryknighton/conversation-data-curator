"""Define the Pydantic data schemas."""
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    content: str


class Message(MessageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ReadMessages(BaseModel):
    search: Optional[str]
    limit: Optional[int]
    offset: Optional[int]
    sort_by: Optional[str]
    sort_asc: Optional[bool]


class CreateMessage(MessageBase):
    pass


class UpdateMessage(MessageBase):
    id: int


class DeleteItem(BaseModel):
    id: int
