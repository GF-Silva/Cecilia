from pydantic import BaseModel, Field
from .validations import AIModelName

class ChatPayload(BaseModel):
    model: AIModelName = Field(min_length=1)

class MessageCreatePayload(BaseModel):
    text: str = Field(min_length=1)
