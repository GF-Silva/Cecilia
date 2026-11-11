from dataclasses import dataclass
from pydantic import BaseModel
from typing import Literal

class Reasoning(BaseModel):
    type: Literal['summary', 'encrypted', 'text']
    format: str
    encrypted_data: str | None = None
    signature: str | None = None
    text: str | None = None
    id: str | None = None
    index: int | None = None

@dataclass
class SSEResponse:
    event: Literal["finished", "error", "message", "reasoning"]
    chunk: str | None = None
    full_response: str | None = None
    reasoning: list[Reasoning] | None = None
    raw_reasoning: str | None = None