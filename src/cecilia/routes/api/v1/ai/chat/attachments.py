from fastapi import APIRouter
from .dependencies import AttachmentServiceDep
from cecilia.models.attachment_model import AttachmentCreate, AttachmentPublic
from .schemas import AttachmentCreatePayload

router = APIRouter(prefix="/{message_id}/attachments")

@router.post("", response_model=list[AttachmentPublic])
def create_attachment(
    message_id: int,
    attachment_service: AttachmentServiceDep,
    attachments_create: list[AttachmentCreatePayload]
):
    db_attachments_create = [
        AttachmentCreate(
            message_id=message_id,
            **attachment.model_dump()
        ) for attachment in attachments_create
    ]

    db_attachments = attachment_service.create_list(
        message_id=message_id,
        attachments=db_attachments_create
    )

    return db_attachments

@router.get("/{attachment_id}", response_model=AttachmentPublic)
def get_attachment_data(
    attachment_id: int,
    attachment_service: AttachmentServiceDep
):
    db_attachment = attachment_service.show(attachment_id)

    return db_attachment