from .attachment_service import AttachmentService
from .message_service import MessageService
from .chat_service import ChatService
from .reasoning_service import ReasoningService
from fastapi import Depends
from typing import Annotated
from cecilia.repositories import AttachmentRepositoryDep, MessageRepositoryDep, ChatRepositoryDep, ReasoningRepositoryDep

def get_attachment_service(
    attachment_repo: AttachmentRepositoryDep
):
    return AttachmentService(attachment_repo)

def get_chat_service(chat_repository: ChatRepositoryDep):
    return ChatService(chat_repository)

def get_message_service(
        message_repository: MessageRepositoryDep
    ):
    return MessageService(message_repository)

def get_reasoning_service(reasoning_repository: ReasoningRepositoryDep):
    return ReasoningService(reasoning_repository)

AttachmentServiceDep = Annotated[AttachmentService, Depends(get_attachment_service)]
MessageServiceDep = Annotated[MessageService, Depends(get_message_service)]
ReasoningServiceDep = Annotated[ReasoningService, Depends(get_reasoning_service)]
ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]