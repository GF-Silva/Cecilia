from sqlmodel import SQLModel
from .attachment_model import AttachmentBase
from uuid import UUID

class MessageBase(SQLModel):
    is_user: bool = True
    chat_id: UUID
    text: str | None = None

class MessagePublic(MessageBase):
    id: int
    attachments: list[AttachmentBase]

class MessageCreate(MessageBase):
    pass