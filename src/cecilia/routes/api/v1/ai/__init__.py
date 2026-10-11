from fastapi import APIRouter
from .tts import router as tts_router
from .llm import router as llm_router

router = APIRouter()

router.include_router(tts_router, prefix="/tts", tags=["TTS"])
router.include_router(llm_router, prefix="/llm", tags=["LLM"])