from fastapi import APIRouter
from .ai import router as ai_router
from .chat import router as chat_router

router = APIRouter()

router.include_router(ai_router, prefix='/ai')
router.include_router(chat_router, prefix="/chat", tags=["Chat"])