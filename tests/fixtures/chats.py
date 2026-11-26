import pytest
from cecilia.models import ChatCreate, Chat
import uuid
from datetime import datetime, UTC

@pytest.fixture
def chat_create():
    def _factory(
        user_id: int = 1
    ):
        return ChatCreate(user_id=user_id)

    return _factory

@pytest.fixture
def chat(chat_create):
    def _factory(
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        id: uuid.UUID | None = None,
        **kwargs
    ):
        return Chat(
            **chat_create(**kwargs).model_dump(),
            created_at=created_at if created_at is not None else datetime.now(UTC),
            updated_at=updated_at if updated_at is not None else datetime.now(UTC),
            id=id if id is not None else uuid.uuid7()
        )

    return _factory
