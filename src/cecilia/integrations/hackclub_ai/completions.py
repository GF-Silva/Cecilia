from cecilia.core.settings import settings
from httpx_sse import aconnect_sse, EventSource
from .types.payload import CompletionEvent
from .types.responses import SSEResponse, Data
from .types.messages import Message
import difflib
from . import errors

class Completions:
    ERROR_MAP = {
        400: {
            'input required: specify "prompt" or  "messages"': 'messages_empty',
            'is not a valid model ID': 'invalid_model_id'
        },
        402: {
            'Spending limit reached. Needs higher limit? hey@mahadk.com': 'spending_limit_reached'
        },
        404: {
            'cannot be used with the chat/completions endpoint': 'unsuported_model_for_endpoint'
        }
    }
    
    async def create(self, model: str, messages: list[Message]):
        headers = {
            "Authorization": f"Bearer {settings.hackclub_ai.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": messages,
            "stream": True
        }

        async with aconnect_sse(
            client=settings.api_client,
            method='POST',
            url=settings.hackclub_ai.completions_url,
            headers=headers,
            json=payload
        ) as event_source:

            content_type = event_source.response.headers.get("content-type", "")

            if "application/json" in content_type:
                if event_source.response.is_success:
                    print("success response, why this is even here?")
                    return
        
                await event_source.response.aread()
                data = event_source.response.json()

                error = data.get("error")

                if not error:
                    print("error not found")
                    raise errors.HackClubBaseError(
                        message="unexpected error",
                        code="internal_server_error"
                    )

                error_message = error.get("message") if isinstance(error, dict) else error

                if not error_message:
                    print("error message not found, crash")
                    raise errors.HackClubBaseError(
                        message="unexpected error",
                        code="internal_server_error"
                    )

                status_code = event_source.response.status_code
                error_cases = list(self.ERROR_MAP[status_code].keys())

                matches = difflib.get_close_matches(error_message, error_cases, n=1, cutoff=0.4)
        
                if not matches:
                    print("matches not found")
                    raise errors.HackClubBaseError(
                        message="unexpected error",
                        code="internal_server_error"
                    )

                match self.ERROR_MAP[status_code][matches[0]]:
                    case "messages_empty":
                        raise errors.MessagesEmptyError(
                            messages=messages,
                            code="messages_empty"
                        )

                    case "invalid_model_id":
                        raise errors.InvalidModelIDError(
                            model_id=model,
                            code="invalid_model_id"
                        )

                    case "spending_limit_reached":
                        raise errors.SpendingLimitReachedError(code="spending_limit_reached")

                    case "unsuported_model_for_endpoint":
                        raise errors.UnsuportedModelForEndpointError(
                            model=model,
                            code="unsuported_model_for_endpoint"
                        )

                    case _:
                        print("default error code")
                        raise errors.HackClubBaseError(
                            message="unexpected error",
                            code="internal_server_error"
                        )
                
            elif "text/event-stream" in content_type:
                
                async for sse in event_source.aiter_sse():
                    if sse.data == "[DONE]":
                        yield SSEResponse(
                            event="finished"
                        )
                        break
        
                    data = CompletionEvent.from_json(sse.data)
        
                    yield SSEResponse(
                        event="message",
                        data=Data(
                            chunk=data.choices[0].delta.content
                        )
                    )