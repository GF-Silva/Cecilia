from .client import client
from cecilia.core.settings import settings
from .models import ContentsModel, AIModelName
from .schemas.sse import EventPayload, EventData

class Chat:
    def __init__(self):
        print("Init OpenRouter Chat")

        self.context = []

    async def send(self, model: AIModelName, contents: ContentsModel):
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

            self.context.append({
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
                    *self.context
                ],
                stream=True
            )

            response = ""

            async for chunk in stream:
                if chunk.choices[0].finish_reason:
                    yield EventPayload(
                        event="finished"
                    )
                    break

                delta_content = chunk.choices[0].delta.content

                if delta_content:
                    response += delta_content

                    yield EventPayload(
                        data=EventData(
                            message="Chunk generated",
                            chunk=delta_content
                        ),
                        event='chunk_generated'
                    )
            
            self.context.append({
                "role": "assistant",
                "content": response
            })

        except Exception as error:
            raise error