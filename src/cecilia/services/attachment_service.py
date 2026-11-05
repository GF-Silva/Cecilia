from cecilia.repositories import AttachmentRepository
from cecilia.models.attachment_model import AttachmentCreate, AttachmentPublic
from cecilia.models.tables import Attachment
from collections.abc import Sequence
from cecilia.core.exceptions import NotFoundError, UnsupportedFileFormatError

class AttachmentService:
    ACCEPTED_TYPES = frozenset(['audio/mpeg', 'audio/x-aiff', 'audio/aac', 'audio/ogg'])

    def __init__(
            self, 
            attachment_repository: AttachmentRepository
        ):
        self.attachment_repository = attachment_repository

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

    def create(self, attachment: AttachmentCreate) -> AttachmentPublic:
        self.validate_mime_type(attachment.mime_type)
        
        db_attachment = self.attachment_repository.create(attachment)

        return self._to_attachment_public(db_attachment)

    def create_list(self, attachments: list[AttachmentCreate]) -> list[Attachment]:
        # Validate the file
        for attachment in attachments:
            self.validate_mime_type(attachment.mime_type)

        db_attachments = self.attachment_repository.create_list(attachments)
            
        return db_attachments

    def validate_mime_type(self, mime_type: str):
        if not mime_type in self.ACCEPTED_TYPES:
            raise UnsupportedFileFormatError(
                message=f"{mime_type} is not supported",
                values={
                    "supported_types": list(self.ACCEPTED_TYPES),
                    "mime_type": mime_type
                }
            )

    def delete(self, id: int):
        attachment = self.show(id)

        self.attachment_repository.delete(attachment)

        return True

    def _to_attachment_public(self, attachment: Attachment) -> AttachmentPublic:
        return AttachmentPublic.model_validate(attachment)