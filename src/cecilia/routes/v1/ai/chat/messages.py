from fastapi import APIRouter
from .dependencies import MessageServiceDep
from cecilia.models.message_model import MessageCreate, MessagePublic
from .schemas import MessageCreatePayload

router = APIRouter(prefix="/{chat_id}/messages")

@router.post("", response_model=MessagePublic)
def create_message(
    chat_id: int,
    message_service: MessageServiceDep,
    message_create: MessageCreatePayload
):
    db_message_create = MessageCreate(
        chat_id=chat_id,
        **message_create.model_dump()
    )

    db_message = message_service.create(db_message_create)

    return db_message

@router.get("", response_model=list[MessagePublic])
def get_messages(
    chat_id: int,
    message_service: MessageServiceDep,
    limit: int = 100,
    offset: int = 0
):
    messages = message_service.get_all_by_chat_id(
        chat_id=chat_id,
        limit=limit,
        offset=offset
    )

    return messages

@router.get("/{message_id}", response_model=MessagePublic)
def get_message_data(
    message_id: int,
    message_service: MessageServiceDep,
):
    db_message = message_service.show(message_id)

    return db_message