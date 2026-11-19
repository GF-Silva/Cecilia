from cecilia.repositories import AttachmentRepository
from cecilia.models.attachment_model import AttachmentCreate, AttachmentPublic, AttachmentUpdate
from cecilia.models.tables import Attachment, Message
from collections.abc import Sequence
from cecilia.core.exceptions import NotFoundError, RuleError

class AttachmentService:
    def __init__(
            self, 
            attachment_repository: AttachmentRepository
        ):
        self.attachment_repository = attachment_repository

    def show(self, id: int, message_id: int) -> Attachment:
        attachment = self.attachment_repository.show(id, message_id)

        if not attachment:
            raise NotFoundError(
                resource="attachment",
                item=id
            )

        return attachment

    def index(self, offset: int = 0, limit: int = 100) -> Sequence[Attachment]:
        return self.attachment_repository.index(offset, limit)

    def create(self, attachment: AttachmentCreate, message: Message) -> AttachmentPublic:
        if not message.is_user:
            raise RuleError(
                message = 'Attachments can only be added to user messages',
                values={
                    "message_role": 'user' if message.is_user else 'assistant'
                }
            )

        db_attachment = self.attachment_repository.create(attachment)
        return self._to_attachment_public(db_attachment)

    def create_list(self, attachments: list[AttachmentCreate], message: Message) -> list[Attachment]:
        self.validate_message_role(message)
        db_attachments = self.attachment_repository.create_list(attachments)
        return db_attachments

    def validate_message_role(self, message: Message):
        if not message.is_user:
            raise RuleError(
                message = 'Attachments can only be added to user messages',
                values={
                    "message_role": 'user' if message.is_user else 'assistant'
                }
            )

    def delete(self, id: int, message_id: int):
        attachment = self.show(id, message_id)
        self.attachment_repository.delete(attachment)
        return True

    def update(self, id: int, message_id: int, attachment_update: AttachmentUpdate):
        attachment = self.show(id, message_id)
        return self.attachment_repository.update(db_attachment=attachment, attachment_update=attachment_update)

    def _to_attachment_public(self, attachment: Attachment) -> AttachmentPublic:
        return AttachmentPublic.model_validate(attachment)