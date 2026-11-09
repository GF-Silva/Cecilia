from dataclasses import dataclass
from typing import Literal
from .payload import ReasoningDetails

@dataclass
class SSEResponse:
    event: Literal["finished", "error", "message", "reasoning"]
    chunk: str | None = None
    full_response: str | None = None
    reasoning: list[ReasoningDetails] | None = None