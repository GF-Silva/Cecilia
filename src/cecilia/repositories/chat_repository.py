from cecilia.models.chat_model import ChatCreate, ChatUpdate
from cecilia.models.tables import Chat
from collections.abc import Sequence
from sqlmodel import select, Session

class ChatRepository:
    def __init__(self, session: Session):
        self.session = session

    def index(self, offset: int = 0, limit: int = 100) -> Sequence[Chat]:
        return self.session.exec(select(Chat).offset(offset).limit(limit)).all()

    def show(self, id: int) -> Chat | None:
        return self.session.get(Chat, id)

    def create(self, chat: ChatCreate) -> Chat:
        db_chat = Chat.model_validate(chat)

        self.session.add(db_chat)
        self.session.commit()
        self.session.refresh(db_chat)

        return db_chat

    def update(self, db_chat: Chat, chat_update: ChatUpdate) -> Chat:
        chat_data = chat_update.model_dump(exclude_unset=True)
        db_chat.sqlmodel_update(chat_data)

        self.session.add(db_chat)
        self.session.commit()
        self.session.refresh(chat_data)

        return db_chat