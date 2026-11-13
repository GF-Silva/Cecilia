from dataclasses import dataclass
from pydantic import BaseModel
from typing import Literal
from enum import StrEnum

class Reasoning(BaseModel):
    type: Literal['summary', 'encrypted', 'text']
    format: str
    encrypted_data: str | None = None
    signature: str | None = None
    text: str | None = None
    id: str | None = None
    index: int | None = None

class Event(StrEnum):
    FINISHED = 'finished'
    ERROR = 'error'
    MESSAGE = 'message'
    REASONING = 'reasoning'

@dataclass
class Response:
    text: str | None = None
    reasonings: list[Reasoning] | None = None

@dataclass
class SSEResponse:
    event: Event
    chunk: str | None = None
    reasoning: list[Reasoning] | None = None
    raw_reasoning: str | None = None