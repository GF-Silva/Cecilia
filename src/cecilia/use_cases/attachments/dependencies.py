from cecilia.integrations import R2IntegrationDep
from cecilia.validators import FileValidatorDep
from cecilia.services import AttachmentServiceDep
from .create import CreateAttachmentsUseCase
from .delete import AttachmentDeleteUseCase
from typing import Annotated
from fastapi import Depends

def get_attachment_delete_use_case(
    r2_integration: R2IntegrationDep,
    attachment_service: AttachmentServiceDep
):
    return #TODO: Re-add it AttachmentDeleteUseCase(r2_integration=r2_integration, attachments_service=attachment_service)

def get_create_attachments_use_case(
    attachment_service: AttachmentServiceDep,
    r2_integration: R2IntegrationDep,
    file_validator: FileValidatorDep
):
    return CreateAttachmentsUseCase(
        attachment_service=attachment_service, 
        r2_integration=r2_integration,
        file_validator=file_validator
    )

CreateAttachmentsUseCaseDep = Annotated[CreateAttachmentsUseCase, Depends(get_create_attachments_use_case)]
AttachmentDeleteUseCaseDep = Annotated[AttachmentDeleteUseCase, Depends(get_attachment_delete_use_case)]