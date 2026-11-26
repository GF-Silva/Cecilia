from cecilia.facades import AttachmentShowFacade
from cecilia.models import AttachmentPublic
from .payloads import AttachmentShowPayload

class AttachmentShowUseCase:
    def __init__(self, attachment_show_facade: AttachmentShowFacade):
        self.attachment_show_facade = attachment_show_facade

    def __call__(self, payload: AttachmentShowPayload) -> AttachmentPublic:
        db_attachment = self.attachment_show_facade(
            user_id=payload.user_id,
            chat_id=payload.chat_id,
            message_id=payload.message_id,
            attachment_id=payload.attachment_id
        )

        return AttachmentPublic.model_validate(db_attachment.model_dump())