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

Content = TextContent | AudioContent

@dataclass
class Message:
    role: str
    content: list[Content]