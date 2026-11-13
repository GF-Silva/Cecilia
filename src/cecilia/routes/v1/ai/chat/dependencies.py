# Core elements
from cecilia.core.database import SessionDep
from cecilia.core.settings import settings
from cecilia.core.exceptions import InternalError

# Repositories
from cecilia.repositories import ChatRepository, MessageRepository, AttachmentRepository, ReasoningRepository

# Services
from cecilia.services import ChatService, MessageService, AttachmentService, ReasoningService

# Integrations
from cecilia.integrations import Completions, R2, r2_manager

# Use cases
from cecilia.use_cases import CreateAttachmentsUseCase, SendChatMessagesUseCase, SaveAssistantAnswerUseCase

# Builders
from cecilia.builders import DBToOpenrouterMessageBuilder

# Adapters
from cecilia.adapters.ffprobe.ffprobe_adapter import FFProbeAdapter

# Python libs
from fastapi import Depends
from typing import Annotated

# TODO: Separar as dependencies em diversos arquivos de alto nivel nas suas respectivas classes

def get_chat_repository(session: SessionDep):
    yield ChatRepository(session)

def get_message_repository(session: SessionDep):
    yield MessageRepository(session)

def get_attachment_repository(session: SessionDep):
    yield AttachmentRepository(session)

def get_reasoning_repository(session: SessionDep):
    yield ReasoningRepository(session)

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
    if not r2_manager.client:
        raise InternalError()
    
    yield R2(r2_manager.client)

def get_ffprobe_adapter():
    yield FFProbeAdapter()

def get_create_attachments_use_case(
    attachment_service: AttachmentServiceDep,
    r2_integration: R2IntegrationDep,
    ffprobe_adapter: FFProbeAdapter = Depends(get_ffprobe_adapter)
):
    yield CreateAttachmentsUseCase(attachment_service, r2_integration, ffprobe_adapter)

def get_reasoning_service(reasoning_repository: ReasoningRepository = Depends(get_reasoning_repository)):
    yield ReasoningService(reasoning_repository)

def get_save_assistant_answer_use_case(
    message_service: MessageServiceDep,
    reasoning_service: ReasoningServiceDep
):
    yield SaveAssistantAnswerUseCase(message_service=message_service, reasoning_service=reasoning_service)

def get_db_to_openrouter_message_builder(
    r2_integration: R2IntegrationDep
):
    yield DBToOpenrouterMessageBuilder(r2_integration=r2_integration)

def get_send_chat_messages_use_case(
    completions_integration: HCAICompletionIntegrationDep,
    message_service: MessageServiceDep,
    save_assistant_answer_use_case: SaveAssistantAnswerUseCase = Depends(get_save_assistant_answer_use_case),
    db_to_openrouter_message_builder: DBToOpenrouterMessageBuilder = Depends(get_db_to_openrouter_message_builder)
):
    yield SendChatMessagesUseCase(
        completions_integration=completions_integration,
        message_service=message_service,
        db_to_openrouter_message_builder=db_to_openrouter_message_builder,
        save_assistant_answer_use_case=save_assistant_answer_use_case
    )

MessageServiceDep = Annotated[MessageService, Depends(get_message_service)]
ReasoningServiceDep = Annotated[ReasoningService, Depends(get_reasoning_service)]
ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
AttachmentServiceDep = Annotated[AttachmentService, Depends(get_attachment_service)]
HCAICompletionIntegrationDep = Annotated[Completions, Depends(get_hcai_completion_integration)]
R2IntegrationDep = Annotated[R2, Depends(get_r2_integration)]
CreateAttachmentsUseCaseDep = Annotated[CreateAttachmentsUseCase, Depends(get_create_attachments_use_case)]
SendChatMessagesUseCaseDep = Annotated[SendChatMessagesUseCase, Depends(get_send_chat_messages_use_case)]