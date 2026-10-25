from cecilia.repositories import MessageRepository, ChatRepository
from cecilia.models.message_model import MessageCreate, MessagePublic
from cecilia.models.tables import Message

from collections.abc import Sequence

class MessageService:
    def __init__(
        self, 
        message_repository: MessageRepository,
        chat_repository: ChatRepository
    ):
        self.message_repository = message_repository
        self.chat_repository = chat_repository

    def show(self, id: int) -> Message:
        db_message = self.message_repository.show(id)

        if not db_message:
            raise LookupError('mensagem não encontrada')

        return db_message

    def get_all_by_chat_id(self, chat_id: int, offset: int = 0, limit: int = 100) -> Sequence[Message]:
        # Verifica se o chat existe
        db_chat = self.chat_repository.show(chat_id)

        if not db_chat:
            raise LookupError("chat not found")

        return self.message_repository.get_all_by_chat_id(
            chat_id=chat_id,
            offset=offset,
            limit=limit
        )

    def index(self, offset: int = 0, limit: int = 100) -> Sequence[Message]:
        return self.message_repository.index(offset, limit)

    def create(self, message_data: MessageCreate) -> MessagePublic:
        db_chat = self.chat_repository.show(message_data.chat_id)

        if not db_chat:
            raise LookupError("chat not found for the given chat_id")

        db_message = self.message_repository.create(message_data)

        return self._to_message_public(db_message)

    def _to_message_public(self, message: Message) -> MessagePublic:
        return MessagePublic.model_validate(message)