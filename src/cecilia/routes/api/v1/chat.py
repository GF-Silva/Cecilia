from fastapi import APIRouter
from pydantic import BaseModel, Field
from collections.abc import AsyncIterable
from fastapi.sse import EventSourceResponse, ServerSentEvent

from cecilia.integrations.open_router import Chat
from cecilia.integrations.open_router.models import ContentsModel, AIModelName

class Request(BaseModel):
    contents: ContentsModel
    model: AIModelName = Field(min_length=1)

router = APIRouter()
chat = Chat()

@router.post("", response_class=EventSourceResponse)
async def send(request: Request):
    try:
        stream = chat.send(request.model, request.contents)

        async for chunk in stream:
            yield ServerSentEvent(data=chunk.data, event=chunk.event)
        
    except Exception as error:
        print("Erro: ", error)
        yield ServerSentEvent(event='error')

@router.get("")
def get_context():
    return chat.context