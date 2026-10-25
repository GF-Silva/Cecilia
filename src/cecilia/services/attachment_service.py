from cecilia.repositories import AttachmentRepository, MessageRepository
from cecilia.models.attachment_model import AttachmentCreate, AttachmentPublic
from cecilia.models.tables import Attachment
from collections.abc import Sequence

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
            raise LookupError("Attachment não encontrado")

        return attachment

    def index(self, offset: int = 0, limit: int = 100) -> Sequence[Attachment]:
        return self.attachment_repository.index(offset, limit)

    def create(self, attachment: AttachmentCreate) -> Attachment:
        db_message = self.message_repository.show(attachment.message_id)

        if not db_message:
            raise LookupError("message not found for the given message_id")
            
        return self.attachment_repository.create(attachment)

    def delete(self, id: int):
        attachment = self.attachment_repository.show(id)

        if not attachment:
            raise LookupError("attachment não encontrado para esse ID")

        self.attachment_repository.delete(attachment)

        return True

    def _to_attachment_public(self, attachment: Attachment) -> AttachmentPublic:
        return AttachmentPublic.model_validate(attachment)