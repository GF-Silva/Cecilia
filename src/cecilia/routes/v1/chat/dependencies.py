# Core elements
from cecilia.core.settings import settings
from cecilia.core.exceptions import InternalError

# Services
from cecilia.services import ChatServiceDep, MessageServiceDep, AttachmentServiceDep, ReasoningServiceDep

# Integrations
from cecilia.integrations import HCAICompletionIntegrationDep, R2IntegrationDep

# Use cases
from cecilia.use_cases import CreateAttachmentsUseCase, SendChatMessagesUseCase

# Collectors
from cecilia.collectors import CompletionCollector

# Builders
from cecilia.builders import DBToOpenrouterMessageBuilder

# Adapters
from cecilia.adapters import FFProbeAdapterDep

# Validators
from cecilia.validators import AudioValidatorDep, ImageValidatorDep

# Python libs
from fastapi import Depends
from typing import Annotated

# TODO: Separar as dependencies em diversos arquivos de alto nivel nas suas respectivas classes

def get_create_attachments_use_case(
    attachment_service: AttachmentServiceDep,
    r2_integration: R2IntegrationDep,
    ffprobe_adapter: FFProbeAdapterDep,
    audio_validator: AudioValidatorDep,
    image_validator: ImageValidatorDep
):
    yield CreateAttachmentsUseCase(
        attachment_service, 
        r2_integration, 
        ffprobe_adapter, 
        image_validator=image_validator,
        audio_validator=audio_validator
    )

def get_completion_collector(
    message_service: MessageServiceDep,
    reasoning_service: ReasoningServiceDep
):
    yield CompletionCollector(message_service=message_service, reasoning_service=reasoning_service)

def get_db_to_openrouter_message_builder(
    r2_integration: R2IntegrationDep
):
    yield DBToOpenrouterMessageBuilder(r2_integration=r2_integration)

def get_send_chat_messages_use_case(
    completions_integration: HCAICompletionIntegrationDep,
    message_service: MessageServiceDep,
    completion_collector: CompletionCollector = Depends(get_completion_collector),
    db_to_openrouter_message_builder: DBToOpenrouterMessageBuilder = Depends(get_db_to_openrouter_message_builder)
):
    yield SendChatMessagesUseCase(
        completions_integration=completions_integration,
        message_service=message_service,
        db_to_openrouter_message_builder=db_to_openrouter_message_builder,
        completion_collector=completion_collector
    )

CreateAttachmentsUseCaseDep = Annotated[CreateAttachmentsUseCase, Depends(get_create_attachments_use_case)]
SendChatMessagesUseCaseDep = Annotated[SendChatMessagesUseCase, Depends(get_send_chat_messages_use_case)]