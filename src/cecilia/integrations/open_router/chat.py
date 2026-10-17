from .client import client
from cecilia.core.settings import settings
from .types import Contents, Event, EventData

class Chat:
    def __init__(self):
        print("Init OpenRouter Chat")

    async def send(self, model: str, contents: Contents, context):
        try:
            user_request = []

            if contents.prompt:
                user_request.append({
                    "type": "text",
                    "text": contents.prompt
                })

            if contents.audios:
                for audio in contents.audios:
                    user_request.append({
                        "type": "input_audio",
                        "input_audio": {
                            "data": audio.data,
                            "format": audio.format
                        }
                    })

            if contents.images:
                print("Ignorando imagens, sem suporte ainda...")

            context.append({
                "role": "user",
                "content": user_request
            })

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

            context.append({
                "role": "assistant",
                "content": response
            })

        except Exception as error:
            raise error