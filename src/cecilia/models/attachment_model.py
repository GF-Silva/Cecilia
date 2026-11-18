from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class AttachmentBase(SQLModel):
    mime_type: str
    size: int | None = None
    filename: uuid.UUID = Field(default_factory=uuid.uuid7) # TODO: This should be an internal property
    message_id: int
    public_filename: str | None = None
    is_valid: bool | None = False

    @property
    def path(self) -> str:
        return f"{self.mime_type}/{self.filename}"    

class AttachmentUpdate(AttachmentBase):
    pass

class AttachmentPublic(AttachmentBase):
    id: int
    created_at: datetime

class AttachmentCreate(AttachmentBase):
    pass