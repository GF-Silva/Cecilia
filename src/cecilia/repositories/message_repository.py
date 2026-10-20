from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from collections.abc import Sequence

from cecilia.models.message_model import MessageCreate
from cecilia.models.tables import Message

class MessageRepository:
    def __init__(self, session: Session):
        self.session = session

    def index(self, offset: int = 0, limit: int = 100) -> Sequence[Message]:
        return self.session.exec(
            select(Message)
            .offset(offset)
            .limit(limit)
        ).all()

    def show(self, id: int) -> Message | None:
        return self.session.get(Message, id)

    def get_all_by_chat_id(self, chat_id: int, limit: int = 100, offset: int = 0) -> Sequence[Message]:
        return self.session.exec(
            select(Message)
            .options(selectinload(Message.attachments)) # pyright: ignore[reportArgumentType]
            .where(Message.chat_id == chat_id)
            .offset(offset)
            .limit(limit)
        ).all()

    def create(self, message_data: MessageCreate):
        db_message = Message.model_validate(message_data)
        self.session.add(db_message)
        self.session.commit()
        self.session.refresh(db_message)

        return db_message