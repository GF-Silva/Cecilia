from fastapi import APIRouter, UploadFile, File, Depends
from .dependencies import AttachmentServiceDep, CreateAttachmentsUseCaseDep
from cecilia.models.attachment_model import AttachmentPublic
from cecilia.models.tables import Message
from .validations import get_message

router = APIRouter(prefix="/attachments", tags=['Attachments'])

@router.post("", response_model=list[AttachmentPublic])
async def create_attachment(
    message_id: int,
    create_attachments_use_case: CreateAttachmentsUseCaseDep,
    message: Message = Depends(get_message),
    files: list[UploadFile] = File(...)
):
    return await create_attachments_use_case(
        message_id=message_id, 
        files=files,
        message=message
    )

@router.get("/{attachment_id}", response_model=AttachmentPublic)
def get_attachment_data(
    attachment_id: int,
    message_id: int,
    attachment_service: AttachmentServiceDep
):
    db_attachment = attachment_service.show(attachment_id, message_id)

    return db_attachment