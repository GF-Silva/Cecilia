from sqlmodel import SQLModel, Field

class ReasoningBase(SQLModel):
    message_id: int
    text: str | None = None

class ReasoningCreate(ReasoningBase):
    type: str # summary, text, encrypted
    format: str
    encrypted_data: str | None = None  
    reasoning_id: str | None = None
    signature: str | None = None
    index: int | None = None

class ReasoningPublic(ReasoningBase):
    id: int