from fastapi import APIRouter
from .ai import router as ai_router

router_v1 = APIRouter()

router_v1.include_router(ai_router, prefix='/ai')