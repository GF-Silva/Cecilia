""" TODO:
usar o id da completion como id do SSE?
Nao, vou criar um proprio pra n depender da resposta da hackclub
"""








from cecilia.core.settings import settings
from httpx_sse import aconnect_sse
from .types.payload import CompletionEvent
from .types.responses import SSEResponse, Data

class Completions:
    async def create(self, model: str, messages: list[dict]):
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

            match content_type:
                case "application/json":
                    await event_source.response.aread()
                    data = event_source.response.json()
                    
                    return

                case "text/event-stream":

                    response = ""
                    async for sse in event_source.aiter_sse():
                        if sse.data == "[DONE]":
                            yield SSEResponse(
                                event="finished",
                                raw_data=response
                            )
                            break

                        data = CompletionEvent.from_json(sse.data)

                        response += data.choices[0].delta.content

                        yield SSEResponse(
                            event="message",
                            data=Data(
                                chunk=data.choices[0].delta.content
                            )
                        )