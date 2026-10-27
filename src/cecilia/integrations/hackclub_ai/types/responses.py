from dataclasses import dataclass
from typing import Literal

@dataclass
class Data:
    chunk: str | None = None

@dataclass
class SSEResponse:
    event: Literal["finished", "error", "message"]
    data: Data | None = None
    raw_data: str | None = None