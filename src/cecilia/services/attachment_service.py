from cecilia.repositories.attachment_repository import AttachmentRepository, Attachment, AttachmentCreate, AttachmentPublic

class AttachmentService:
    def __init__(self, attachment_repository: AttachmentRepository):
        self.attachment_repository = attachment_repository

    def show(self, id: int) -> Attachment:
        attachment = self.attachment_repository.show(id)

        if not attachment:
            raise ValueError("Attachment não encontrado")

        return attachment

    def index(self, offset: int = 0, limit: int = 100) -> list[Attachment | None]:
        return self.attachment_repository.index(offset, limit)

    def create(self, attachment: AttachmentCreate):
        # Simula conexao com a class MessageRepository

        # message = self.message_repository.show(attachment.message_id)
        message = True

        if not message:
            raise ValueError("Menssagem não encontrada")

        return self.attachment_repository.create(attachment)

    def delete(self, id: int):
        attachment = self.attachment_repository.show(id)

        if not attachment:
            raise ValueError("attachment não encontrado para esse ID")

        self.attachment_repository.delete(attachment)

        return True