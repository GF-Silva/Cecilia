from sqlmodel import Session, select
from collections.abc import Sequence

from cecilia.models.message_model import Message, MessageCreate

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

    def create(self, message_data: MessageCreate):
        db_message = Message.model_validate(message_data)
        self.session.add(db_message)
        self.session.commit()
        self.session.refresh(db_message)

        return db_message