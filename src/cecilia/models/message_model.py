from sqlmodel import SQLModel
from .attachment_model import AttachmentBase

class MessageBase(SQLModel):
    role: str
    chat_id: int
    content: str | None = None

class MessagePublic(MessageBase):
    id: int
    attachments: list[AttachmentBase]

class MessageCreate(MessageBase):
    pass