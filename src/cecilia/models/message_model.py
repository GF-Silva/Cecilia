from sqlmodel import SQLModel
from .attachment_model import AttachmentPublic
from .reasoning_model import ReasoningPublic
from uuid import UUID

class MessageBase(SQLModel):
    is_user: bool = True
    chat_id: UUID
    text: str | None = None

class MessagePublic(MessageBase):
    id: int
    attachments: list[AttachmentPublic]
    reasonings: list[ReasoningPublic]

class MessageCreate(MessageBase):
    pass