from cecilia.models.attachment_model import AttachmentCreate, AttachmentUpdate
from cecilia.models.tables import Attachment
from collections.abc import Sequence

class FakeAttachmentRepository:
    def __init__(self):
        print("Repository created")
        self.storage = {}
        self._counter = 1

    def create(self, attachment: AttachmentCreate) -> Attachment:
        new_id = self._counter
        self._counter += 1
        db_attachment = Attachment(id=new_id, **attachment.model_dump())
        self.storage[new_id] = db_attachment
        return db_attachment

    def create_list(self, attachments: list[AttachmentCreate]) -> list[Attachment]:
        db_attachments: list[Attachment] = [
            self.create(attachment)
            for attachment in attachments
        ]

        return db_attachments

    def show(self, id: int, message_id: int) -> Attachment | None:
        attachment = self.storage.get(id)
        return attachment if attachment and attachment.message_id == message_id else None

    def update(self, attachment_update: AttachmentUpdate, db_attachment: Attachment) -> Attachment:
        attachment_data = attachment_update.model_dump(exclude_unset=True)
        db_attachment.sqlmodel_update(attachment_data)
        self.storage[db_attachment.id] = db_attachment
        return db_attachment

    def index(self, offset: int = 0, limit: int = 100) -> Sequence[Attachment]:
        return list(self.storage.values())[offset:offset + limit]

    def delete(self, attachment: Attachment):
        self.storage.pop(attachment.id)
        return True