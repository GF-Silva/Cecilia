from httpx import ReadTimeout, WriteTimeout, ConnectTimeout, PoolTimeout
from fastapi.sse import EventSourceResponse, ServerSentEvent
from collections.abc import AsyncIterable
from fastapi import APIRouter
from uuid import UUID

from .schemas import ChatPayload
from .dependencies import SendChatMessagesUseCaseDep
from cecilia.core.exceptions import BaseError

router = APIRouter(prefix="/completions", tags=['Completions'])

@router.post("", response_class=EventSourceResponse)
async def create_completion(
    chat_id: UUID,
    send_chat_messages_use_case: SendChatMessagesUseCaseDep,
    chat_payload: ChatPayload,
) -> AsyncIterable[ServerSentEvent]:
    try:
        response_stream = send_chat_messages_use_case(
            chat_id=chat_id,
            model=chat_payload.model,
            effort=chat_payload.effort
        )

        async for stream, response in response_stream:
            yield ServerSentEvent(
                data=stream if not response else None,
                raw_data=response if response else None,
                event=stream.event
            )

    except BaseError as err:
        print("base error: ", err)
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
        yield ServerSentEvent(
            event='error',
            data={
                "message": "something unexpected happened, maybe try again after a while?", 
                "error_code": "INTERNAL_ERROR", 
                "status_code": 500, 
                "title": "Internal Server Error"
            }
        )