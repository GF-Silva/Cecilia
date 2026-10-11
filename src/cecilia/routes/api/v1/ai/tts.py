from src.cecilia.integrations.azure import TTS
from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel

router = APIRouter()

tts = TTS()

class AudioRequest(BaseModel):
    text: str

@router.post("/")
def synthesize_text(request: AudioRequest):
    audio: bytes = tts.synthesize(request.text)

    return Response(
        content = audio,
        media_type="audio/webm",
        headers={"Content-Disposition": 'inline'}
    )