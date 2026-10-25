from fastapi import APIRouter
from fastapi.sse import EventSourceResponse, ServerSentEvent
from collections.abc import AsyncIterable

from .schemas import ChatPayload
from .dependencies import ChatServiceDep, MessageServiceDep, OpenRouterIntegrationDep

from cecilia.models.chat_model import ChatCreate, ChatPublic
from cecilia.models.message_model import MessagePublic, MessageCreate

from cecilia.integrations.open_router.types import Message, Content, Audio

router = APIRouter(prefix="/chats")

@router.post("", response_model=ChatPublic)
def create_new_chat(
    chat_data: ChatCreate,
    chat_service: ChatServiceDep
):
    return chat_service.create(chat_data)

@router.post("/{chat_id}", response_class=EventSourceResponse)
async def send_prompt(
    chat_id: int,
    message_service: MessageServiceDep,
    chat_payload: ChatPayload,
    open_router_integration: OpenRouterIntegrationDep
):
    try:
        db_messages = message_service.get_all_by_chat_id(chat_id)

        messages: list[Message]  = []

        # Construir cada mensagem
        for msg in db_messages:
            contents: list[Content] = []

            if msg.attachments:
                for attachment in msg.attachments:
                    if attachment.type == "audio":
                        audio = Audio(
                            format=attachment.format,
                            data=attachment.data
                        )

                        contents.append(Content(
                            type="input_audio",
                            input_audio=audio
                        ))

                    if attachment.type == "image":
                        print("fds")

            if msg.text:
                contents.append(Content(
                    type="text",
                    text=msg.text
                ))

            message = Message(
                role=msg.role,
                content=contents
            )

            messages.append(message)
        
        stream = open_router_integration.send(
            model=chat_payload.model,
            context=messages
        )

        response = ""

        async for chunk in stream:
            if chunk.event == "finished":
                response = chunk.raw_data

            yield ServerSentEvent(
                data=chunk.data,
                event=chunk.event
            )

        message_service.create(MessageCreate(
            role="assistant",
            chat_id=chat_id,
            text=response
        ))
    
    except Exception as err:
        yield ServerSentEvent(
            data=str(err),
            event="error"
        )