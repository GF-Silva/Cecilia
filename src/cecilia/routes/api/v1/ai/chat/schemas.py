from pydantic import BaseModel, ConfigDict, Field, model_validator, AfterValidator
from typing import Annotated
import re

def check_ai_model_name(name: AIModelName) -> AIModelName:
    regex = r'^[A-Za-z0-9~._:@+-]+/[A-Za-z0-9~._:@+-]+$'
    
    if not re.match(regex, name):
        raise ValueError('o nome está mal formatado, siga o formato provedor-legal/nome-do-modelo')

    return name

AIModelName = Annotated[str, AfterValidator(check_ai_model_name)]

class AudioPayload(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )
    data: str = Field(min_length=1)
    format: str = Field(min_length=1) # TODO: Validar quais formatos a API aceita e deixar apenas eles passarem

class ContentsPayload(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )
    prompt: str | None = Field(default=None, min_length=1)
    audios: list[AudioPayload] | None = Field(default=None, min_length=1)
    images: list | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_optional_fields(self) -> "ContentsPayload":
        if not self.prompt and not self.audios and not self.images:
            raise ValueError("ao menos um campo opcional deve ser preenchido")

        return self

class ChatPayload(BaseModel):
    contents: ContentsPayload
    model: AIModelName = Field(min_length=1)
    user_id: int