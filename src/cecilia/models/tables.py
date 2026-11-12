from sqlmodel import Field, Relationship
from datetime import datetime, UTC
import uuid

from .attachment_model import AttachmentBase
from .message_model import MessageBase
from .chat_model import ChatBase
from .reasoning_model import ReasoningBase

class Attachment(AttachmentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    size: int | None = Field(default=None, index=True)
    filename: uuid.UUID
    path: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    message_id: int = Field(foreign_key="message.id", index=True)
    message: Message = Relationship(back_populates="attachments")

class Reasoning(ReasoningBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    message_id: int = Field(foreign_key='message.id', index=True)
    message: Message = Relationship(back_populates='reasonings')
    type: str # summary, text, encrypted
    format: str
    encrypted_data: str | None = None  
    reasoning_id: str | None = None
    signature: str | None = None
    index: int | None = None

class Message(MessageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    chat_id: uuid.UUID = Field(foreign_key="chat.id")
    attachments: list[Attachment] | None = Relationship(back_populates="message", cascade_delete=True)
    reasonings: list[Reasoning] | None = Relationship(back_populates='message', cascade_delete=True)

class Chat(ChatBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid7, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(UTC)
        }
    )