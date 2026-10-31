from pydantic import BaseModel, Field
from .validations import AIModelName

class ChatPayload(BaseModel):
    model: AIModelName = Field(min_length=1)

class MessageCreatePayload(BaseModel):
    text: str = Field(min_length=1)

class AttachmentCreatePayload(BaseModel):
    type: str = Field(min_length=1)
    format: str = Field(min_length=1)
    data: str = Field(min_length=1)
    size: str | None = Field(default=None, min_length=1)