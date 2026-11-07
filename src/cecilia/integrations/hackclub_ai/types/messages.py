from dataclasses import dataclass

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

@dataclass
class Message:
    role: str
    content: list[Content]