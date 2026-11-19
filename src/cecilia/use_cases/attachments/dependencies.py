from cecilia.integrations import R2IntegrationDep
from cecilia.validators import FileValidatorDep
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
    file_validator: FileValidatorDep
):
    return CreateAttachmentsUseCase(
        attachment_service=attachment_service, 
        r2_integration=r2_integration,
        file_validator=file_validator
    )

CreateAttachmentsUseCaseDep = Annotated[CreateAttachmentsUseCase, Depends(get_create_attachments_use_case)]
DeleteAttachmentUseCaseDep = Annotated[DeleteAttachmentUseCase, Depends(get_delete_attachment_use_case)]