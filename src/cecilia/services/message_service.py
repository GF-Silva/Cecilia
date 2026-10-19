from cecilia.repositories import MessageRepository
from cecilia.models.message_model import Message, MessageCreate, MessagePublic

from collections.abc import Sequence

class MessageService:
    def __init__(self, message_repository: MessageRepository):
        self.message_repository = message_repository

    def show(self, id: int) -> Message:
        db_message = self.message_repository.show(id)

        if not db_message:
            raise ValueError('mensagem não encontrada')

        return db_message

    def index(self, offset: int = 0, limit: int = 100) -> Sequence[Message]:
        return self.message_repository.index(offset, limit)

    def create(self, message_data: MessageCreate) -> MessagePublic:
        db_message = self.message_repository.create(message_data)

        return self._to_message_public(db_message)

    def _to_message_public(self, message: Message) -> MessagePublic:
        return MessagePublic.model_validate(message)