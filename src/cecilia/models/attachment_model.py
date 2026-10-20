from sqlmodel import Field, SQLModel
from datetime import datetime, UTC

class AttachmentBase(SQLModel):
    type: str
    data: str
    size: str | None = Field(default=None)
    message_id: int

class AttachmentPublic(AttachmentBase):
    id: int
    created_at: datetime

class AttachmentCreate(AttachmentBase):
    pass