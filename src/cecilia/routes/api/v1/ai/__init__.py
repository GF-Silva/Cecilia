from fastapi import APIRouter
from .llm import router as llm_router
from .chat import router as chat_router

router = APIRouter()

router.include_router(llm_router, prefix="/llm", tags=["LLM"])
router.include_router(chat_router, tags=["Chat"])