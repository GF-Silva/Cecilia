from fastapi import APIRouter
from fastapi.sse import EventSourceResponse, ServerSentEvent
from collections.abc import AsyncIterable
from dataclasses import asdict

from .schemas import ChatPayload
from .dependencies import (
    ChatServiceDep, 
    MessageServiceDep,
    HCAICompletionIntegrationDep
)

from cecilia.models.chat_model import ChatCreate, ChatPublic
from cecilia.models.message_model import MessageCreate

from cecilia.integrations.hackclub_ai.types.messages import (
    Message, 
    TextContent, 
    AudioContent,
    Content,
    Audio
)

from cecilia.integrations.hackclub_ai import errors

router = APIRouter(prefix="/chats")

@router.post("", response_model=ChatPublic)
def create_new_chat(
    chat_data: ChatCreate,
    chat_service: ChatServiceDep
):
    return chat_service.create(chat_data)

@router.post("/{chat_id}/completions", response_class=EventSourceResponse)
async def create_completion(
    chat_id: int,
    completions: HCAICompletionIntegrationDep,
    message_service: MessageServiceDep,
    chat_payload: ChatPayload
) -> AsyncIterable[ServerSentEvent]:
    try:
        db_messages = message_service.get_all_by_chat_id(chat_id)

        if not db_messages:
            raise errors.MessagesEmptyError(db_messages)

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

        response = ""
        async for stream_event in stream:
            response += stream_event.data.chunk if stream_event.data and stream_event.data.chunk else ''

            yield ServerSentEvent(
                data=stream_event.data,
                event=stream_event.event
            )

        # TODO: I have to remove this, this is just for visualization and needs to be removed when
        # shipping the final version for the frontend
        yield ServerSentEvent(
            raw_data=response,
            event="response"
        )

        message_service.create(MessageCreate(
            role="assistant",
            chat_id=chat_id,
            text=response
        ))

    except (
        errors.MessagesEmptyError, 
        errors.InvalidModelIDError,
        errors.SpendingLimitReachedError,
        errors.HackClubBaseError
    ) as err:
        print(err)
        yield ServerSentEvent(
            raw_data=str(err),
            event="error"
        )

    except Exception as err:
        print("uncaught exception: ", type(err))
        print("How this happened? Oh man, we are doomed")