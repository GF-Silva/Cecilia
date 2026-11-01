from cecilia.core.database import SessionDep
from cecilia.repositories import ChatRepository, MessageRepository, AttachmentRepository
from cecilia.services import ChatService, MessageService, AttachmentService
from cecilia.integrations.hackclub_ai.completions import Completions
from cecilia.core.settings import settings

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
        message_repository: MessageRepository = Depends(get_message_repository)
    ):
    yield MessageService(message_repository)

def get_attachment_service(
    attachment_repository: AttachmentRepository = Depends(get_attachment_repository)
):
    yield AttachmentService(attachment_repository)

def get_hcai_completion_integration():
    yield Completions(
        api_key=settings.hackclub_ai.api_key,
        completions_url=settings.hackclub_ai.completions_url,
        api_client=settings.api_client
    )

MessageServiceDep = Annotated[MessageService, Depends(get_message_service)]
ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
AttachmentServiceDep = Annotated[AttachmentService, Depends(get_attachment_service)]
HCAICompletionIntegrationDep = Annotated[Completions, Depends(get_hcai_completion_integration)]