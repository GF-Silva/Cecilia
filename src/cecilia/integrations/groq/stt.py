from .client import client
from cecilia.core.settings import settings

class STT:
    def __init__(self):
        print("Init Azure STT")

    async def transcript(self, filename: str, file_content: bytes, content_type: str | None = None):
        transcription = await client.audio.transcriptions.create(
            file=(filename, file_content),
            model=settings.groq.stt_model,
            language=settings.groq.stt_language
        )

        return transcription