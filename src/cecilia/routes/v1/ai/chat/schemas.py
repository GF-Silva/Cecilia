from pydantic import BaseModel, Field
from cecilia.integrations.hackclub_ai.types.messages import Effort
from .validations import AIModelName

class ChatPayload(BaseModel):
    model: AIModelName = Field(min_length=1)
    effort: Effort | None = None

class MessageCreatePayload(BaseModel):
    text: str = Field(min_length=1)
