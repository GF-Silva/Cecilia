from httpx import ReadTimeout, WriteTimeout, ConnectTimeout, PoolTimeout
from fastapi.sse import EventSourceResponse, ServerSentEvent
from collections.abc import AsyncIterable
from fastapi import APIRouter

from .schemas import ChatPayload
from .dependencies import SendChatMessagesUseCaseDep

from cecilia.core.exceptions import BaseError

router = APIRouter(prefix="/completions")

@router.post("", response_class=EventSourceResponse)
async def create_completion(
    chat_id: int,
    send_chat_messages_use_case: SendChatMessagesUseCaseDep,
    chat_payload: ChatPayload,
) -> AsyncIterable[ServerSentEvent]:
    try:
        response_stream = send_chat_messages_use_case(
            chat_id=chat_id,
            model=chat_payload.model
        )

        async for stream in response_stream:
            yield ServerSentEvent(
                data=stream.chunk,
                raw_data=stream.full_response,
                event=stream.event
            )

    except BaseError as err:
        yield ServerSentEvent(
            data=err,
            event="error"
        )

    except (ReadTimeout, WriteTimeout, ConnectTimeout, PoolTimeout):
        yield ServerSentEvent(
            event="error",
            data={
                "message": "Timed out",
                "code": "timeout"
            }
        )

    except Exception as err:
        print("uncaught exception: ", err)
        print("How this happened? Oh man, we are doomed")