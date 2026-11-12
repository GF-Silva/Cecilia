from sqlmodel import SQLModel
from datetime import datetime
import uuid

class AttachmentBase(SQLModel):
    mime_type: str
    size: int | None = None
    message_id: int
    public_filename: str | None = None

class AttachmentPublic(AttachmentBase):
    id: int
    created_at: datetime

class AttachmentCreate(AttachmentBase):
    filename: uuid.UUID
    path: str