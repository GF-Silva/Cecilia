from fastapi import APIRouter
from collections.abc import AsyncIterable
from fastapi.sse import EventSourceResponse, ServerSentEvent

from cecilia.integrations.open_router import Chat
from .schemas import ChatPayload

router = APIRouter()
chat = Chat()

@router.post("", response_class=EventSourceResponse)
async def send(request: ChatPayload):
    try:
        stream = chat.send(request.model, request.contents.to_openrouter_contents())

        async for chunk in stream:
            yield ServerSentEvent(data=chunk.data, event=chunk.event)
        
    except Exception as error:
        print("Erro: ", error)
        yield ServerSentEvent(event='error')

@router.get("")
def get_context():
    return chat.context