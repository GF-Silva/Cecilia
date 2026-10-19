from sqlmodel import Field, SQLModel
from datetime import datetime, UTC

class AttachmentBase(SQLModel):
    type: str
    data: str
    size: str | None = Field(default=None)
    message_id: int

class Attachment(AttachmentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

class AttachmentPublic(AttachmentBase):
    id: int
    created_at: datetime

class AttachmentCreate(AttachmentBase):
    pass