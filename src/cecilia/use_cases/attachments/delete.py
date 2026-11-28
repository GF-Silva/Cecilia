from cecilia.integrations import R2 
from cecilia.services import AttachmentService
from cecilia.models.attachment_model import AttachmentPublic
from cecilia.facades import AttachmentModifyFacade
from .payloads import AttachmentShowPayload

class AttachmentDeleteUseCase:
    def __init__(
        self,
        r2_integration: R2,
        attachments_service: AttachmentService,
        attachment_modify_facade: AttachmentModifyFacade
    ):
        self.r2_integration = r2_integration
        self.attachments_service = attachments_service
        self.attachment_modify_facade = attachment_modify_facade

    async def __call__(self, payload: AttachmentShowPayload):
        self.attachment_modify_facade(
            user_id=payload.user_id,
            chat_id=payload.chat_id,
            message_id=payload.message_id,
            attachment_id=payload.attachment_id
        )

        attachment = self.attachments_service.invalidate(
            id=payload.attachment_id,
            message_id=payload.message_id
        )

        await self.r2_integration.delete_file(path=attachment.path)

        return AttachmentPublic.model_validate(attachment.model_dump())