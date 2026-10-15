from pydantic import BaseModel, ConfigDict, Field, model_validator, AfterValidator
from typing import Annotated
from .client import guest_client
import re

def check_ai_model_name(name: AIModelName) -> AIModelName:
    regex = r'^[A-Za-z0-9~._:@+-]+/[A-Za-z0-9~._:@+-]+$'
    
    if not re.match(regex, name):
        raise ValueError('o nome está mal formatado, siga o formato provedor-legal/nome-do-modelo')

    return name

AIModelName = Annotated[str, AfterValidator(check_ai_model_name)]

def ai_model_exists(name: str) -> bool:
    try:
        author, slug = name.split('/')
        return guest_client.models.get(author=author, slug=slug) is not None
    
    except:
        return False

class MediaModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )
    data: str = Field(min_length=1)
    format: str = Field(min_length=1) # TODO: Validar quais formatos a API aceita e deixar apenas eles passarem

class ContentsModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )
    prompt: str | None = Field(default=None, min_length=1)
    audios: list[MediaModel] | None = Field(default=None, min_length=1)
    images: list[MediaModel] | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_optional_fields(self) -> "ContentsModel":
        if not self.prompt and not self.audios and not self.images:
            raise ValueError("ao menos um campo opcional deve ser preenchido")

        return self