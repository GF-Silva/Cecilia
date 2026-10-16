from dataclasses import dataclass
from typing import Literal

@dataclass
class ContentsAudios:
    format: str
    data: str

@dataclass
class Contents:
    prompt: str | None = None
    audios: list[ContentsAudios] | None = None
    images: list[ContentsAudios] | None = None

@dataclass
class EventData:
    chunk: str | None = None
    message: str | None = None

@dataclass
class Event:
    event: Literal["finished", "error", "chunk_generated"]
    data: EventData | None = None

