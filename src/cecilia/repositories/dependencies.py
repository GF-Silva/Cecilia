from .attachment_repository import AttachmentRepository
from .message_repository import MessageRepository
from .chat_repository import ChatRepository
from .reasoning_repository import ReasoningRepository
from cecilia.core.database import SessionDep
from fastapi import Depends
from typing import Annotated

def get_attachment_repository(
    session: SessionDep
):
    return AttachmentRepository(session)

def get_message_repository(session: SessionDep):
    return MessageRepository(session)

def get_chat_repository(session: SessionDep):
    return ChatRepository(session)

def get_reasoning_repository(session: SessionDep):
    return ReasoningRepository(session)

AttachmentRepositoryDep = Annotated[AttachmentRepository, Depends(get_attachment_repository)]
MessageRepositoryDep = Annotated[MessageRepository, Depends(get_message_repository)]
ChatRepositoryDep = Annotated[ChatRepository, Depends(get_chat_repository)]
ReasoningRepositoryDep = Annotated[ReasoningRepository, Depends(get_reasoning_repository)]
