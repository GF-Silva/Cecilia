# junta tudo da v1
from fastapi import APIRouter
from .chat import router as chat_router

router_v1 = APIRouter()

router_v1.include_router(chat_router, prefix='/chat', tags=['Chat'])