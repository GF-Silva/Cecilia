from pydantic import BaseModel, ConfigDict, Field, model_validator, AfterValidator
from typing import Annotated
import re

from cecilia.integrations.open_router.types import Contents as OpenRouterContents, ContentsAudios

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

    def to_openrouter_audio(self) -> ContentsAudios:
        return ContentsAudios(
            data = self.data,
            format = self.format
        )

class ContentsModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )
    prompt: str | None = Field(default=None, min_length=1)
    audios: list[AudioPayload] | None = Field(default=None, min_length=1)
    images: list | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_optional_fields(self) -> "ContentsModel":
        if not self.prompt and not self.audios and not self.images:
            raise ValueError("ao menos um campo opcional deve ser preenchido")

        return self

    def to_openrouter_contents(self) -> OpenRouterContents:
        openrouter_audios = (
            [audio.to_openrouter_audio() for audio in self.audios]
            if self.audios is not None
            else None
        )
        
        return OpenRouterContents(
            prompt = self.prompt,
            audios = openrouter_audios,
            images = self.images
        )

class ChatPayload(BaseModel):
    contents: ContentsModel
    model: AIModelName = Field(min_length=1)