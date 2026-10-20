from fastapi import APIRouter
from fastapi.sse import EventSourceResponse, ServerSentEvent
from collections.abc import AsyncIterable

from cecilia.integrations.open_router import Chat
from .schemas import ChatPayload
from .mapper import to_openrouter_contents

from .dependencies import ChatServiceDep, MessageServiceDep, AttachmentServiceDep

from cecilia.models.chat_model import ChatCreate, ChatPublic
from cecilia.models.message_model import MessagePublic

router = APIRouter()

@router.post("", response_model=ChatPublic)
def create_new_chat(
    chat_data: ChatCreate,
    chat_service: ChatServiceDep
):
    return chat_service.create(chat_data)

@router.post("/{id}")
def send_prompt(
    id: int,
    chat_service: ChatServiceDep,
    chat_payload: ChatPayload
):
    return chat_service.show(id)