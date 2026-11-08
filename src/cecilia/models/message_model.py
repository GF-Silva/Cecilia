from sqlmodel import SQLModel
from .attachment_model import AttachmentBase
from .reasoning_model import ReasoningBase
from uuid import UUID

class MessageBase(SQLModel):
    is_user: bool = True
    chat_id: UUID
    text: str | None = None

class MessagePublic(MessageBase):
    id: int
    attachments: list[AttachmentBase]
    reasonings: list[ReasoningBase]

class MessageCreate(MessageBase):
    pass