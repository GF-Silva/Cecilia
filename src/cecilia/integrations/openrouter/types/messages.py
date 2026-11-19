from dataclasses import dataclass
from typing import Literal, Annotated
from enum import StrEnum
from pydantic import BaseModel, Field

@dataclass
class Audio:
    format: str
    data: str

@dataclass
class TextContent:
    text: str
    type: str = "text"

@dataclass
class AudioContent:
    input_audio: Audio
    type: str = "input_audio"

@dataclass
class ImageUrl:
    url: str

@dataclass
class ImageContent:
    image_url: ImageUrl
    type: str = "image_url"

Content = TextContent | AudioContent | ImageContent

class Effort(StrEnum):
    NONE='none'
    MINIMAL='minimal'
    LOW='low'
    MEDIUM='medium'
    HIGH='high'
    XHIGH='xhigh'
    MAX='max'

class BaseReasoningDetails(BaseModel):
    format: str
    id: str | None = None
    index: int | None = None

class SummaryReasoning(BaseReasoningDetails):
    summary: str
    type: Literal['reasoning.summary'] = 'reasoning.summary'

class EncryptedReasoning(BaseReasoningDetails):
    type: Literal['reasoning.encrypted'] = 'reasoning.encrypted'
    data: str

class TextReasoning(BaseReasoningDetails):
    type: Literal['reasoning.text'] = 'reasoning.text'
    text: str | None = None
    signature: str | None = None

Reasoning = Annotated[
    TextReasoning | EncryptedReasoning | SummaryReasoning,
    Field(discriminator='type')
]

class Message(BaseModel):
    role: Literal['user', 'assistant', 'system']
    content: list[Content]
    reasoning_details: list[Reasoning] | None = None