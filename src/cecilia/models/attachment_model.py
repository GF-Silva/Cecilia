from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class AttachmentBase(SQLModel):
    mime_type: str
    size: int | None = None
    filename: uuid.UUID = Field(default_factory=uuid.uuid7)
    message_id: int
    public_filename: str | None = None

    @property
    def path(self) -> str:
        return f"{self.mime_type}/{self.filename}"    

class AttachmentPublic(AttachmentBase):
    id: int
    created_at: datetime

class AttachmentCreate(AttachmentBase):
    pass