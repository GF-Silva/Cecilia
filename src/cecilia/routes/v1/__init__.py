from fastapi import APIRouter
from .ai import router as ai_router

router = APIRouter()

router.include_router(ai_router, prefix='/ai')