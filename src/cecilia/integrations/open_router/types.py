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
    raw_data: str | None = None

    def __post_init__(self):
        if self.data and self.raw_data:
            raise ValueError('Os campos "data" e "raw_data" não devem estar definidos ao mesmo tempo')

