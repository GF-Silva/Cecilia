from pydantic import BaseModel, Field, AfterValidator, create_model
from typing import Annotated
import re

def check_ai_model_name(name: AIModelName) -> AIModelName:
    regex = r'^[A-Za-z0-9~._:@+-]+/[A-Za-z0-9~._:@+-]+$'
    
    if not re.match(regex, name):
        raise ValueError('o nome está mal formatado, siga o formato provedor-legal/nome-do-modelo')

    return name

AIModelName = Annotated[str, AfterValidator(check_ai_model_name)]

class ChatPayload(BaseModel):
    model: AIModelName = Field(min_length=1)

class MessageCreatePayload(BaseModel):
    role: str = Field(min_length=1)
    text: str = Field(min_length=1)

class AttachmentCreatePayload(BaseModel):
    type: str = Field(min_length=1)
    format: str = Field(min_length=1)
    data: str = Field(min_length=1)
    size: str | None = Field(default=None, min_length=1)