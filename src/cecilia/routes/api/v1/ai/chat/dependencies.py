from cecilia.core.database import SessionDep
from cecilia.repositories import ChatRepository, MessageRepository, AttachmentRepository
from cecilia.services import ChatService, MessageService, AttachmentService

from fastapi import Depends
from typing import Annotated

def get_chat_repository(session: SessionDep):
    yield ChatRepository(session)

def get_message_repository(session: SessionDep):
    yield MessageRepository(session)

def get_attachment_repository(session: SessionDep):
    yield AttachmentRepository(session)

def get_chat_service(chat_repository: ChatRepository = Depends(get_chat_repository)):
    yield ChatService(chat_repository)

def get_message_service(
        message_repository: MessageRepository = Depends(get_message_repository),
        chat_repository: ChatRepository = Depends(get_chat_repository)
    ):
    yield MessageService(message_repository, chat_repository)

def get_attachment_service(
    attachment_repository: AttachmentRepository = Depends(get_attachment_repository),
    message_service: MessageService = Depends(get_message_service)
):
    yield AttachmentService(attachment_repository, message_service)

MessageServiceDep = Annotated[MessageService, Depends(get_message_service)]
ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
AttachmentServiceDep = Annotated[AttachmentService, Depends(get_attachment_service)]