from sqlmodel import SQLModel, Field

class MessagesBase(SQLModel):
    role: str
    chat_id: int

class Messages(MessagesBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: str | None = Field(default=None, index=True)

class MessagesPublic(MessagesBase):
    id: int
    timestamp: str

class MessagesCreate(MessagesBase):
    pass