from pydantic import BaseModel
from cecilia.integrations.openrouter.types.responses import Event

class Response(BaseModel):
    event: Event
    chunk: str | None = None
    reasoning: list[str] | None = None