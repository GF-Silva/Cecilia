from sqlmodel import SQLModel, Field

class ChatsBase(SQLModel):
    user_id: int | None = Field(default=None, index=True)

class Chats(ChatsBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: str | None = None
    updated_at: str | None = None

class ChatsPublic(ChatsBase):
    id: int
    created_at: str
    updated_at: str

class ChatsCreate(ChatsBase):
    pass

class ChatsUpdate(ChatsBase):
    user_id: int | None = None