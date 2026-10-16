from fastapi import APIRouter
from collections.abc import AsyncIterable
from fastapi.sse import EventSourceResponse

from cecilia.integrations.open_router import Chat
from cecilia.integrations.open_router.types import Event
from .schemas import ChatPayload
from .mapper import to_openrouter_contents

router = APIRouter()
chat = Chat()

@router.post("", response_class=EventSourceResponse)
async def send(request: ChatPayload) -> AsyncIterable[Event]:
    try:
        stream = chat.send(request.model, to_openrouter_contents(request.contents))

        async for chunk in stream:
            yield chunk
        
    except Exception as error:
        print("Erro: ", error)
        yield Event(event='error')

@router.get("")
def get_context():
    return chat.context