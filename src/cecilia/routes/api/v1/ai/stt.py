from cecilia.integrations.groq import STT
from fastapi import APIRouter, UploadFile, File, HTTPException
import mimetypes

router = APIRouter()

stt = STT()

@router.post("/")
async def transcript_audio(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith('audio'):
        raise HTTPException(status_code=400, detail="O arquivo entregue não é um audio")

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(status_code=400, detail="Arquivo vazio")

    filename = file.filename or f"audio{mimetypes.guess_extension(file.content_type) or '.wav'}"
    transcription = await stt.transcript(filename, file_bytes, file.content_type)

    return transcription