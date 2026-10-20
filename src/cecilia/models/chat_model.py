from sqlmodel import SQLModel, Field
from datetime import UTC, datetime

class ChatBase(SQLModel):
    user_id: int | None = Field(default=None, index=True)

class ChatPublic(ChatBase):
    id: int
    created_at: datetime
    updated_at: datetime

class ChatCreate(ChatBase):
    pass

class ChatUpdate(ChatBase):
    user_id: int | None = None