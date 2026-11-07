from sqlmodel import SQLModel, Field
from datetime import UTC, datetime
from uuid import UUID

class ChatBase(SQLModel):
    user_id: int | None = Field(default=None)

class ChatPublic(ChatBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

class ChatCreate(ChatBase):
    pass

class ChatUpdate(ChatBase):
    user_id: int | None = None