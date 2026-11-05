from fastapi import APIRouter, UploadFile, File
from .dependencies import AttachmentServiceDep, CreateAttachmentsUseCaseDep
from cecilia.models.attachment_model import AttachmentPublic

router = APIRouter(prefix="/attachments")

@router.post("", response_model=list[AttachmentPublic])
async def create_attachment(
    message_id: int,
    create_attachments_use_case: CreateAttachmentsUseCaseDep,
    files: list[UploadFile] = File(...)
):
    return await create_attachments_use_case.execute(message_id, files)

@router.get("/{attachment_id}", response_model=AttachmentPublic)
def get_attachment_data(
    attachment_id: int,
    attachment_service: AttachmentServiceDep
):
    db_attachment = attachment_service.show(attachment_id)

    return db_attachment