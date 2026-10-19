from fastapi import APIRouter, Depends
from fastapi.sse import EventSourceResponse, ServerSentEvent
from collections.abc import AsyncIterable
from typing import Annotated

from cecilia.integrations.open_router import Chat
from .schemas import ChatPayload
from .mapper import to_openrouter_contents

from cecilia.core.database import SessionDep
from cecilia.repositories import MessageRepository, AttachmentRepository, ChatRepository
from cecilia.services import MessageService, AttachmentService, ChatService
from cecilia.use_cases.create_new_chat import CreateNewChat

router = APIRouter()

# Essa rota é para criar um novo chat, quando o usuario não tem chat criado ainda?

def get_chat_repository(session: SessionDep):
    yield ChatRepository(session)

def get_message_repository(session: SessionDep):
    yield MessageRepository(session)

def get_attachment_repository(session: SessionDep):
    yield AttachmentRepository(session)

def get_chat_service(chat_repository: ChatRepository = Depends(get_chat_repository)):
    yield ChatService(chat_repository)

def get_message_service(
        message_repository: MessageRepository = Depends(get_message_repository),
    ):
    yield MessageService(message_repository)

def get_attachment_service(
    attachment_repository: AttachmentRepository = Depends(get_attachment_repository),
    message_service: MessageService = Depends(get_message_service)
):
    yield AttachmentService(attachment_repository, message_service)

def get_create_new_chat_use_case(
    attachment_service: AttachmentService = Depends(get_attachment_service),
    message_service: MessageService = Depends(get_message_service),
    chat_service: ChatService = Depends(get_chat_service)
):
    yield CreateNewChat(
        attachment_service=attachment_service,
        message_service=message_service,
        chat_service=chat_service,
        open_router_chat=Chat()
    )

CreateNewChatDep = Annotated[CreateNewChat, Depends(get_create_new_chat_use_case)]

@router.post("", response_class=EventSourceResponse)
async def send_without_chat(
    create_new_chat: CreateNewChatDep,
    chat_payload: ChatPayload
):
    new_chat = create_new_chat.execute(
        contents=to_openrouter_contents(chat_payload.contents),
        ai_model=chat_payload.model,
        user_id=chat_payload.user_id
    )

    async for chunk in new_chat:
        yield ServerSentEvent(
            raw_data=chunk.raw_data,
            data=chunk.data,
            event=chunk.event
        )

# @router.post("/", response_class=EventSourceResponse)
# async def send(request: ChatPayload) -> AsyncIterable[ServerSentEvent]:
#     try:

#         # Fake context made for tests
#         context = []

#         stream = chat.send(request.model, to_openrouter_contents(request.contents), context)

#         async for chunk in stream:
#             yield ServerSentEvent(
#                 raw_data=chunk.raw_data,
#                 data=chunk.data,
#                 event=chunk.event
#             )
        
#     except Exception as error:
#         print("Erro: ", error)
        # yield ServerSentEvent(event='error')

# TODO: Fix this
@router.get("")
def get_context():
    return []