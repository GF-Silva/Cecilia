from cecilia.integrations import R2IntegrationDep
from cecilia.validators import AudioValidatorDep, ImageValidatorDep
from cecilia.adapters import FFProbeAdapterDep
from cecilia.services import AttachmentServiceDep
from .delete import DeleteAttachmentUseCase
from .create import CreateAttachmentsUseCase
from typing import Annotated
from fastapi import Depends

def get_delete_attachment_use_case(
    r2_integration: R2IntegrationDep,
    attachment_service: AttachmentServiceDep
):
    return DeleteAttachmentUseCase(r2_integration=r2_integration, attachments_service=attachment_service)

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

CreateAttachmentsUseCaseDep = Annotated[CreateAttachmentsUseCase, Depends(get_create_attachments_use_case)]
DeleteAttachmentUseCaseDep = Annotated[DeleteAttachmentUseCase, Depends(get_delete_attachment_use_case)]