from sqlmodel import SQLModel, Field

class MessageBase(SQLModel):
    role: str
    chat_id: int
    content: str | None = None

class Message(MessageBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class MessagePublic(MessageBase):
    id: int

class MessageCreate(MessageBase):
    pass