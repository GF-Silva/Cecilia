from cecilia.repositories import AttachmentRepository
from cecilia.services.message_service import MessageService
from cecilia.models.attachment_model import Attachment, AttachmentCreate, AttachmentPublic
from collections.abc import Sequence

class AttachmentService:
    def __init__(self, attachment_repository: AttachmentRepository, message_service: MessageService):
        self.attachment_repository = attachment_repository
        self.message_service = message_service

    def show(self, id: int) -> Attachment:
        attachment = self.attachment_repository.show(id)

        if not attachment:
            raise ValueError("Attachment não encontrado")

        return attachment

    def index(self, offset: int = 0, limit: int = 100) -> Sequence[Attachment]:
        return self.attachment_repository.index(offset, limit)

    def create(self, attachment: AttachmentCreate) -> Attachment:
        return self.attachment_repository.create(attachment)

    def delete(self, id: int):
        attachment = self.attachment_repository.show(id)

        if not attachment:
            raise ValueError("attachment não encontrado para esse ID")

        self.attachment_repository.delete(attachment)

        return True

    def _to_attachment_public(self, attachment: Attachment) -> AttachmentPublic:
        return AttachmentPublic.model_validate(attachment)