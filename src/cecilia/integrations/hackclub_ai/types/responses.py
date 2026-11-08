from dataclasses import dataclass
from typing import Literal

@dataclass
class Reasoning:
    content: str | None = None

@dataclass
class SSEResponse:
    event: Literal["finished", "error", "message", "reasoning"]
    chunk: str | None = None
    full_response: str | None = None
    reasoning: list[Reasoning] | None = None