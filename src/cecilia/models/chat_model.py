from sqlmodel import SQLModel, Field
from datetime import UTC, datetime

class ChatBase(SQLModel):
    user_id: int | None = Field(default=None, index=True)

class Chat(ChatBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(UTC)
        }
    )

class ChatPublic(ChatBase):
    id: int
    created_at: datetime
    updated_at: datetime

class ChatCreate(ChatBase):
    pass

class ChatUpdate(ChatBase):
    user_id: int | None = None