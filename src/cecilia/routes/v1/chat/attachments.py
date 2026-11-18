from cecilia.models.attachment_model import AttachmentPublic
from cecilia.use_cases import CreateAttachmentsUseCaseDep
from fastapi import APIRouter, UploadFile, File, Depends
from cecilia.services import AttachmentServiceDep
from cecilia.core.responses import BaseResponse
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

@router.delete("/{attachment_id}", response_model=BaseResponse)
def delete_attachment(attachment_id: int, message_id: int, attachment_service: AttachmentServiceDep):
    attachment_service.delete(id=attachment_id, message_id=message_id)

    return BaseResponse(
        title='Attachment deleted with success',
        message=f'The attachment {attachment_id} from the message {message_id} was deleted with success',
        values={
            'attachment_id': attachment_id,
            'message_id': message_id
        }
    )

@router.get("/{attachment_id}", response_model=AttachmentPublic)
def get_attachment_data(
    attachment_id: int,
    message_id: int,
    attachment_service: AttachmentServiceDep
):
    db_attachment = attachment_service.show(attachment_id, message_id)

    return db_attachment