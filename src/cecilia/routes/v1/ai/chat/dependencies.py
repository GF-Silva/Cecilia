from cecilia.core.database import SessionDep
from cecilia.repositories import ChatRepository, MessageRepository, AttachmentRepository
from cecilia.services import ChatService, MessageService, AttachmentService
from cecilia.core.exceptions import InternalError
from cecilia.integrations.hackclub_ai.completions import Completions
from cecilia.integrations.cloudflare import clients, r2
from cecilia.use_cases.create_attachments import CreateAttachmentsUseCase
from cecilia.adapters.ffprobe.ffprobe_adapter import FFProbeAdapter
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

def get_r2_integration():
    if not clients.r2_manager.client:
        raise InternalError()
    
    yield r2.R2(clients.r2_manager.client)

def get_ffprobe_adapter():
    yield FFProbeAdapter()

def get_create_attachments_use_case(
    attachment_service: AttachmentServiceDep,
    r2_integration: R2IntegrationDep,
    ffprobe_adapter: FFProbeAdapter = Depends(get_ffprobe_adapter)
):
    yield CreateAttachmentsUseCase(attachment_service, r2_integration, ffprobe_adapter)

MessageServiceDep = Annotated[MessageService, Depends(get_message_service)]
ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
AttachmentServiceDep = Annotated[AttachmentService, Depends(get_attachment_service)]
HCAICompletionIntegrationDep = Annotated[Completions, Depends(get_hcai_completion_integration)]
R2IntegrationDep = Annotated[r2.R2, Depends(get_r2_integration)]
CreateAttachmentsUseCaseDep = Annotated[CreateAttachmentsUseCase, Depends(get_create_attachments_use_case)]