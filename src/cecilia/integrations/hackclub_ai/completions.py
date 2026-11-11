# External libs
from httpx_sse import aconnect_sse
from httpx import AsyncClient
import difflib
import json

# Own libs / modules
from cecilia.core.exceptions import InternalError
from .types.payload import CompletionEvent, ReasoningDetails, TextReasoning, EncryptedReasoning, SummaryReasoning
from .types.responses import SSEResponse, Reasoning
from .types.messages import Message, Effort
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
            'cannot be used with the chat/completions endpoint': 'unsuported_model_for_endpoint',
            'No endpoints found that support input audio': 'model_not_support_audio',
            'No endpoints found that support image input': 'model_not_support_image'
        }
    }

    def __init__(
        self, 
        api_key: str,
        api_client: AsyncClient,
        completions_url: str
    ):
        self.api_key = api_key
        self.api_client = api_client
        self.completions_url = completions_url
    
    async def create(
        self, 
        model: str, 
        messages: list[Message], 
        effort: Effort = Effort.NONE
    ):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "reasoning": {
                "effort": effort
            }
        }

        async with aconnect_sse(
            client=self.api_client,
            method='POST',
            url=self.completions_url,
            headers=headers,
            json=payload
        ) as event_source:

            content_type = event_source.response.headers.get("content-type", "")

            if "application/json" in content_type:
                if event_source.response.is_success:
                    return
        
                await event_source.response.aread()
                data = event_source.response.json()

                error = data.get("error")

                if not error:
                    print("error not found")
                    raise InternalError()

                error_message = error.get("message") if isinstance(error, dict) else error

                if not error_message:
                    print("error message not found, crash")
                    raise InternalError()

                status_code = event_source.response.status_code
                error_cases = list(self.ERROR_MAP[status_code].keys())

                matches = difflib.get_close_matches(error_message, error_cases, n=1, cutoff=0.4)
        
                if not matches:
                    print("HackClub AI (Completions): matches not found")
                    print("Err: ", error_message, status_code)
                    raise InternalError()

                match self.ERROR_MAP[status_code][matches[0]]:
                    case "messages_empty":
                        raise errors.MessagesEmptyError(
                            messages=messages
                        )

                    case "invalid_model_id":
                        raise errors.InvalidModelIDError(
                            model_id=model
                        )

                    case "spending_limit_reached":
                        raise errors.SpendingLimitReachedError()

                    case "unsuported_model_for_endpoint":
                        raise errors.UnsuportedModelForEndpointError(
                            model=model
                        )

                    case 'model_not_support_audio':
                        raise errors.ModelNotSupportAudioError(
                            model=model
                        )

                    case 'model_not_support_image':
                        raise errors.ModelNotSupportImageError(model)

                    case _:
                        raise InternalError()
                
            elif "text/event-stream" in content_type:
                response = ""
                async for sse in event_source.aiter_sse():
                    if sse.data == "[DONE]":
                        yield SSEResponse(
                            event="finished",
                            full_response=response
                        )
                        break
        
                    data = CompletionEvent.model_validate(json.loads(sse.data))
                    response += data.choices[0].delta.content

                    yield SSEResponse(
                        event="message",
                        chunk=data.choices[0].delta.content,
                        reasoning=[
                            Reasoning.model_validate({
                                **reasoning.model_dump(),
                                "type": reasoning.type.split('reasoning.')[1],
                                "text": reasoning.summary if isinstance(reasoning, SummaryReasoning) else reasoning.text if isinstance(reasoning, TextReasoning) else None,
                                "encrypted_data": reasoning.data if isinstance(reasoning, EncryptedReasoning) else None
                            })
                            for reasoning in data.choices[0].delta.reasoning_details
                        ] if data.choices[0].delta.reasoning_details else None
                        # else data.choices[0].delta.reasoning if data.choices[0].delta.reasoning else None
                    )