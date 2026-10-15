from dataclasses import dataclass
from typing import Literal

@dataclass
class EventData:
    chunk: str | None = None
    message: str | None = None

@dataclass
class EventPayload:
    event: Literal["finished", "error", "chunk_generated"]
    data: EventData | None = None

