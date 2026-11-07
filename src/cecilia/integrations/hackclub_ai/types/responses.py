from dataclasses import dataclass
from typing import Literal

@dataclass
class SSEResponse:
    event: Literal["finished", "error", "message"]
    chunk: str | None = None
    full_response: str | None = None