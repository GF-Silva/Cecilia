from sqlmodel import Field, Relationship
from datetime import datetime, UTC
from typing import List

from .attachment_model import AttachmentBase
from .message_model import MessageBase
from .chat_model import ChatBase

class Attachment(AttachmentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    message_id: int = Field(foreign_key="message.id")
    message: Message = Relationship(back_populates="attachments")

class Message(MessageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    chat_id: int = Field(default=None, foreign_key="chat.id")
    attachments: List[Attachment] = Relationship(back_populates="message")

class Chat(ChatBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(UTC)
        }
    )