from fastapi import APIRouter

from .dependencies import (
    ChatServiceDep
)

from cecilia.models.chat_model import ChatCreate, ChatPublic

router = APIRouter(prefix="/chats")

@router.post("", response_model=ChatPublic)
def create_new_chat(
    chat_data: ChatCreate,
    chat_service: ChatServiceDep
):
    return chat_service.create(chat_data)

