from sqlmodel import Field, SQLModel
from datetime import datetime

class AttachmentBase(SQLModel):
    type: str
    format: str
    data: str
    size: str | None = Field(default=None)
    message_id: int = Field(index=True)

class AttachmentPublic(AttachmentBase):
    id: int
    created_at: datetime

class AttachmentCreate(AttachmentBase):
    pass