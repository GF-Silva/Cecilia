from fastapi import APIRouter
from .completions import router as completions_router
from .attachments import router as attachments_router
from .messages import router as msg_router
from .chat import router as chat_router

router = APIRouter()

router.include_router(router=chat_router)
chat_router.include_router(router=msg_router)
chat_router.include_router(router=completions_router)
msg_router.include_router(router=attachments_router)
