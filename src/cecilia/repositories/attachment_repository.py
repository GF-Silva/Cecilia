from cecilia.models.attachment_model import AttachmentCreate
from cecilia.models.tables import Attachment
from sqlmodel import select, Session
from collections.abc import Sequence

class AttachmentRepository:
    def __init__(self, session: Session):
        print("Repository created")
        self.session = session

    def create(self, attachment: AttachmentCreate) -> Attachment:
        db_attachment = Attachment.model_validate(attachment)
        self.session.add(db_attachment)
        self.session.commit()
        self.session.refresh(db_attachment)

        return db_attachment

    def create_list(self, attachments: list[AttachmentCreate]) -> list[Attachment]:
        db_attachments: list[Attachment] = []

        for attachment in attachments:
            db_attachment = Attachment.model_validate(attachment)
            db_attachments.append(db_attachment)
        
        self.session.add_all(db_attachments)
        self.session.flush()
        self.session.commit()

        return db_attachments

    def show(self, id: int) -> Attachment | None:
        return self.session.get(Attachment, id)

    def index(self, offset: int = 0, limit: int = 100) -> Sequence[Attachment]:
        return self.session.exec(select(Attachment).offset(offset).limit(limit)).all()

    def delete(self, attachment: Attachment):
        self.session.delete(attachment)
        self.session.commit()

        return True