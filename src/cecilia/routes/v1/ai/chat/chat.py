"""
TODO:

Validar os dados / campos / especificar os try + exception

trocar a rota de cecilia-ai.com para api.cecilia-ai.com

a rota /chat vai ter /completions e /live, para modo em completion e modo live talk

"""





from fastapi import APIRouter
from fastapi.sse import EventSourceResponse, ServerSentEvent
from collections.abc import AsyncIterable
from dataclasses import asdict

from .schemas import ChatPayload
from .dependencies import (
    ChatServiceDep, 
    MessageServiceDep, 
    OpenRouterIntegrationDep,
    HCAICompletionIntegrationDep
)

from cecilia.models.chat_model import ChatCreate, ChatPublic
from cecilia.models.message_model import MessageCreate
from cecilia.integrations.open_router.types import Message, Audio, AudioContent, TextContent, Content

from cecilia.integrations.hackclub_ai.types.messages import (
    Message, 
    TextContent, 
    AudioContent,
    Content,
    Audio
)

router = APIRouter(prefix="/chats")

@router.post("", response_model=ChatPublic)
def create_new_chat(
    chat_data: ChatCreate,
    chat_service: ChatServiceDep
):
    return chat_service.create(chat_data)

@router.post("/{chat_id}/prompt", response_class=EventSourceResponse)
async def send_prompt(
    chat_id: int,
    message_service: MessageServiceDep,
    chat_payload: ChatPayload,
    open_router_integration: OpenRouterIntegrationDep
):
    try:
        db_messages = message_service.get_all_by_chat_id(chat_id)

        messages: list = []

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

                        contents.append(AudioContent(
                            input_audio=audio
                        ))

                    if attachment.type == "image":
                        print("fds")

            if msg.text:
                contents.append(TextContent(
                    text=msg.text
                ))

            message = Message(
                role=msg.role,
                content=contents
            )

            messages.append(asdict(message))
        
        stream = open_router_integration.send(
            model=chat_payload.model,
            context=messages
        )

        response = ""

        async for chunk in stream:
            if chunk.event == "finished":
                response = chunk.raw_data

            yield ServerSentEvent(
                raw_data=chunk.raw_data,
                data=chunk.data,
                event=chunk.event
            )

        message_service.create(MessageCreate(
            role="assistant",
            chat_id=chat_id,
            text=response
        ))
    
    except (LookupError, ValueError) as err:
        yield ServerSentEvent(
            data=str(err),
            event="error"
        )

@router.post("/completions", response_class=EventSourceResponse)
async def create_completion(
    chat_id: int,
    completions: HCAICompletionIntegrationDep,
    message_service: MessageServiceDep,
    chat_payload: ChatPayload
):
    try:
        db_messages = message_service.get_all_by_chat_id(chat_id)

        # if not db_messages:
        #     raise ValueError("messages empty")

        messages: list = []

        for db_message in db_messages:
            content: list = []

            if db_message.text:
                content.append(TextContent(
                    text=db_message.text
                ))

            if db_message.attachments:
                for attachment in db_message.attachments:
                    if attachment.type == "audio":
                        content.append(AudioContent(
                            input_audio=Audio(
                                format=attachment.format,
                                data=attachment.data
                            )
                        ))

                    if attachment.type == "image":
                        print("ignorando imagem")

            message = Message(
                role=db_message.role,
                content=content
            )

            messages.append(asdict(message))

        stream = completions.create(
            messages=messages,
            model=chat_payload.model
        )

        async for stream_event in stream:
            yield ServerSentEvent(
                data=stream_event.data,
                event=stream_event.event,
                raw_data=stream_event.raw_data
            )

    except Exception as err:
        print(err)
        yield ServerSentEvent(
            raw_data=str(err),
            event="error"
        )