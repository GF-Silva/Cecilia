from sqlmodel import SQLModel, Field

class ReasoningBase(SQLModel):
    type: str # summary, text, encrypted
    format: str
    message_id: int
    encrypted_data: str | None = None  
    reasoning_id: str | None = None
    signature: str | None = None
    index: int | None = None
    text: str | None = None

class ReasoningCreate(ReasoningBase):
    pass

class ReasoningPublic(ReasoningBase):
    id: int
    message_id: int