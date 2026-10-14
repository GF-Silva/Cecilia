from .client import client
from cecilia.core.settings import settings
from .models import ContentsModel, ModelName

class Chat:
    def __init__(self):
        print("Init OpenRouter Chat")

        self.context = []

    async def send(self, model: ModelName, contents: ContentsModel):
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
            delta_content = chunk.choices[0].delta.content

            if delta_content:
                response += delta_content
                yield delta_content
        
        self.context.append({
            "role": "assistant",
            "content": response
        })