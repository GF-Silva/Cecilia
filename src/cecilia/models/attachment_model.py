from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from datetime import datetime
import uuid

class AttachmentBase(SQLModel):
    mime_type: str
    size: int | None = None
    filename: uuid.UUID = Field(default_factory=uuid.uuid7) # TODO: This should be an internal property
    message_id: int
    public_filename: str | None = None
    is_valid: bool | None = None

    @property
    def path(self) -> str:
        return f"{self.mime_type}/{self.filename}"    

class AttachmentUpdate(BaseModel):
    mime_type: str | None = None
    size: int | None = None
    message_id: int | None = None
    public_filename: str | None = None
    is_valid: bool | None = None

class AttachmentPublic(AttachmentBase):
    id: int
    created_at: datetime

class AttachmentCreate(AttachmentBase):
    pass