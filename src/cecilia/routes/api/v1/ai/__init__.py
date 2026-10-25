from fastapi import APIRouter
from .tts import router as tts_router
from .llm import router as llm_router
from .stt import router as stt_router
from .chat import router as chat_router

router = APIRouter()

router.include_router(tts_router, prefix="/tts", tags=["TTS"])
router.include_router(llm_router, prefix="/llm", tags=["LLM"])
router.include_router(stt_router, prefix="/stt", tags=["STT"])
router.include_router(chat_router, tags=["Chat"])