from cecilia.repositories import ChatRepository
from cecilia.models.chat_model import ChatCreate, ChatUpdate, ChatPublic
from cecilia.models.tables import Chat
from cecilia.core.exceptions import NotFoundError
from collections.abc import Sequence
from pydantic import TypeAdapter

class ChatService:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    def index(self) -> Sequence[Chat]:
        return self.chat_repository.index()

    def show(self, id: int) -> ChatPublic:
        db_chat = self.chat_repository.show(id)

        if not db_chat:
            raise NotFoundError(
                resource="chat",
                item=id
            )

        return self._to_public_chat(db_chat)

    def create(self, chat_data: ChatCreate) -> ChatPublic:
        # Tenho q validar se o user existe usando o user repository | service
        db_chat = self.chat_repository.create(chat_data)
        
        return self._to_public_chat(db_chat)

    # Tenho q validar se o user existe usando o user service
    def update(self, id: int, chat_update: ChatUpdate) -> ChatPublic:
        db_chat = self.chat_repository.show(id)

        if not db_chat:
            raise NotFoundError(
                resource="chat",
                item=id
            )

        db_chat_updated = self.chat_repository.update(db_chat, chat_update)

        return self._to_public_chat(db_chat_updated)

    def _to_public_chat(self, chat: Chat) -> ChatPublic:
        return ChatPublic.model_validate(chat)

    def _to_multi_public_chat(self, chats: Sequence[Chat]) -> Sequence[ChatPublic]:
        adapter = TypeAdapter(list[ChatPublic])

        return adapter.validate_python(chats)