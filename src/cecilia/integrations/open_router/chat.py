from .client import client
from cecilia.core.settings import settings
from .types import Contents, Event, EventData, Message

class Chat:
    def __init__(self):
        print("Init OpenRouter Chat")

    async def send(self, model: str, context: list = [Message]):
        try:
            stream = await client.chat.send_async(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": settings.open_router.system_prompt
                    },
                    *context
                ],
                stream=True
            )

            response = ""

            async for chunk in stream:
                if chunk.choices[0].finish_reason:
                    yield Event(
                        event="finished",
                        raw_data=response
                    )
                    break

                delta_content = chunk.choices[0].delta.content

                if delta_content:
                    response += delta_content

                    yield Event(
                        data=EventData(
                            message="Chunk generated",
                            chunk=delta_content
                        ),
                        event='chunk_generated'
                    )

        except Exception as error:
            raise error