from sqlmodel import Field, SQLModel
from datetime import datetime
import uuid

class AttachmentBase(SQLModel):
    mime_type: str
    size: int | None = Field(default=None, index=True)
    message_id: int = Field(index=True)
    public_filename: str | None = None
    filename: uuid.UUID
    path: str

class AttachmentPublic(AttachmentBase):
    id: int
    created_at: datetime

class AttachmentCreate(AttachmentBase):
    pass