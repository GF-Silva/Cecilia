from sqlmodel import Field, Relationship
from datetime import datetime, UTC
import uuid

from .attachment_model import AttachmentBase
from .message_model import MessageBase
from .chat_model import ChatBase

class Attachment(AttachmentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    size: int | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    message_id: int = Field(foreign_key="message.id", index=True)
    message: Message = Relationship(back_populates="attachments")

class Message(MessageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    chat_id: uuid.UUID = Field(foreign_key="chat.id", index=True)
    attachments: list[Attachment] = Relationship(back_populates="message")

class Chat(ChatBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid7, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(UTC)
        }
    )