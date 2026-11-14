from fastapi import Depends
from typing import Annotated

from cecilia.services import AttachmentServiceDep, MessageServiceDep, ReasoningServiceDep
from cecilia.integrations import R2IntegrationDep, HCAICompletionIntegrationDep
from cecilia.adapters import FFProbeAdapterDep
from cecilia.validators import AudioValidatorDep, ImageValidatorDep
from cecilia.collectors import CompletionCollectorDep
from cecilia.builders import DBToOpenrouterMessageBuilderDep

from .create_attachments import CreateAttachmentsUseCase
from .completions.send_chat_messages_use_case import SendChatMessagesUseCase

def get_create_attachments_use_case(
    attachment_service: AttachmentServiceDep,
    r2_integration: R2IntegrationDep,
    ffprobe_adapter: FFProbeAdapterDep,
    audio_validator: AudioValidatorDep,
    image_validator: ImageValidatorDep
):
    return CreateAttachmentsUseCase(
        attachment_service=attachment_service, 
        r2_integration=r2_integration, 
        ffprobe_adapter=ffprobe_adapter, 
        image_validator=image_validator,
        audio_validator=audio_validator
    )

def get_send_chat_messages_use_case(
    completions_integration: HCAICompletionIntegrationDep,
    message_service: MessageServiceDep,
    completion_collector: CompletionCollectorDep,
    db_to_openrouter_message_builder: DBToOpenrouterMessageBuilderDep
):
    return SendChatMessagesUseCase(
        completions_integration=completions_integration,
        message_service=message_service,
        db_to_openrouter_message_builder=db_to_openrouter_message_builder,
        completion_collector=completion_collector
    )

CreateAttachmentsUseCaseDep = Annotated[CreateAttachmentsUseCase, Depends(get_create_attachments_use_case)]
SendChatMessagesUseCaseDep = Annotated[SendChatMessagesUseCase, Depends(get_send_chat_messages_use_case)]