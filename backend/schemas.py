"""Define the Pydantic data schemas."""

from pydantic import BaseModel, ConfigDict


class MessageBase(BaseModel):
    content: str


class Message(MessageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CreateMessage(MessageBase):
    pass


class UpdateMessage(MessageBase):
    id: int


class DeleteItem(BaseModel):
    id: int
