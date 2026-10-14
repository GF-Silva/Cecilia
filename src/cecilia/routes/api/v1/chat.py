from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from cecilia.integrations.open_router import Chat
from cecilia.integrations.open_router.models import ContentsModel, ModelName, ai_model_exists
from pydantic import BaseModel, Field, field_validator
from collections.abc import AsyncIterable

router = APIRouter()

class SendModel(BaseModel):
    contents: ContentsModel
    model: ModelName = Field(min_length=1)

chat = Chat()

@router.post("", response_class=StreamingResponse)
async def send(request: SendModel) -> AsyncIterable[str]:
    stream = chat.send(request.model, request.contents)
    
    async for chunk in stream:
        yield chunk

@router.get("")
def get_context():
    return chat.context