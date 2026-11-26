import pytest
import uuid
from cecilia.models import Message

@pytest.fixture
def message():
    def _factory(
        chat_id: uuid.UUID | None = None,
        is_user: bool = True,
        text: str | None = None,
        id: int = 1
    ):
        return Message(
            is_user=is_user, 
            chat_id=chat_id if chat_id else uuid.uuid7(),
            text=text,
            id=id
        )

    return _factory
