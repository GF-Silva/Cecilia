from cecilia.repositories import AttachmentRepository, MessageRepository
from cecilia.models.attachment_model import AttachmentCreate, AttachmentPublic
from cecilia.models.tables import Attachment
from collections.abc import Sequence
from cecilia.core.exceptions import NotFoundError, ValueError

class AttachmentService:
    def __init__(
            self, 
            attachment_repository: AttachmentRepository, 
            message_repository: MessageRepository
        ):
        self.attachment_repository = attachment_repository
        self.message_repository = message_repository

    def show(self, id: int) -> Attachment:
        attachment = self.attachment_repository.show(id)

        if not attachment:
            raise NotFoundError(
                resource="attachment",
                item=id
            )

        return attachment

    def index(self, offset: int = 0, limit: int = 100) -> Sequence[Attachment]:
        return self.attachment_repository.index(offset, limit)

    def create(self, attachment: AttachmentCreate) -> Attachment:            
        return self.attachment_repository.create(attachment)

    def create_list(self, attachments: list[AttachmentCreate]) -> list[Attachment]:
        db_attachments = []

        for attachment in attachments:
            db_attachment = self.create(attachment)
            db_attachments.append(db_attachment)
        
        return db_attachments

    def delete(self, id: int):
        attachment = self.show(id)

        self.attachment_repository.delete(attachment)

        return True

    def _to_attachment_public(self, attachment: Attachment) -> AttachmentPublic:
        return AttachmentPublic.model_validate(attachment)