from dataclasses import dataclass
from typing import Literal
from enum import StrEnum

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

@dataclass
class Message:
    role: Literal['user', 'assistant', 'system']
    content: list[Content]