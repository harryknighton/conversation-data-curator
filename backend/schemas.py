"""Define the Pydantic data schemas."""

from pydantic import BaseModel, ConfigDict

# -----------------------------------------------------------------------
# Messages


class MessageBase(BaseModel):
    content: str


class Message(MessageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CreateMessage(MessageBase):
    pass


class UpdateMessage(MessageBase):
    id: int


class DeleteMessage(BaseModel):
    id: int


# -----------------------------------------------------------------------
# Codes


class CodeBase(BaseModel):
    code: str


class Code(CodeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CreateCode(CodeBase):
    pass


class UpdateCode(CodeBase):
    id: int


class DeleteCode(CodeBase):
    pass
