from fastapi import APIRouter
from collections.abc import AsyncIterable
from fastapi.sse import EventSourceResponse, ServerSentEvent

from cecilia.integrations.open_router import Chat
from .schemas import ChatPayload
from .mapper import to_openrouter_contents

router = APIRouter()
chat = Chat()

# Essa rota é para criar um novo chat, quando o usuario não tem chat criado ainda?

@router.post("", response_class=EventSourceResponse)
async def send(request: ChatPayload) -> AsyncIterable[ServerSentEvent]:
    try:

        # Fake context made for tests
        context = []

        stream = chat.send(request.model, to_openrouter_contents(request.contents), context)

        async for chunk in stream:
            yield ServerSentEvent(
                raw_data=chunk.raw_data,
                data=chunk.data,
                event=chunk.event
            )
        
    except Exception as error:
        print("Erro: ", error)
        yield ServerSentEvent(event='error')

# TODO: Fix this
@router.get("")
def get_context():
    return []