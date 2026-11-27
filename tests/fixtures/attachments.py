from datetime import datetime, UTC
import pytest
import uuid

from tests.fakes.repositories import FakeAttachmentRepository
from cecilia.services import AttachmentService
from cecilia.models.tables import Attachment, Message
from cecilia.models.attachment_model import AttachmentCreate

@pytest.fixture
def fake_attachment_repo():
    return FakeAttachmentRepository()

@pytest.fixture
def attachment_service(fake_attachment_repo, mocker): # TODO: Substituir esse repo por um veridico
    mock_message_repo = mocker.MagicMock()
    return AttachmentService(attachment_repository=fake_attachment_repo, message_repository=mock_message_repo)

@pytest.fixture
def attachment_create():
    def _factory(
        mime_type: str = 'audio/mpeg',
        message_id: int = 1,
        size: int | None = None,
        filename: uuid.UUID | None = None,
        public_filename: str | None = None,
        is_valid: bool | None = None
    ):
        return AttachmentCreate(
            mime_type=mime_type, 
            message_id=message_id, 
            size=size, 
            filename=filename if filename is not None else uuid.uuid7(),
            public_filename=public_filename,
            is_valid=is_valid
        )
    
    return _factory

@pytest.fixture
def attachment(attachment_create):
    def _factory(
        created_at: datetime | None = None,
        id: int = 1,
        **kwargs
    ):
        return Attachment(
            **attachment_create(**kwargs).model_dump(),
            created_at=created_at if created_at is not None else datetime.now(UTC),
            id=id
        )
    
    return _factory

@pytest.fixture
def attachment_invalid():
    def _factory(db_attachment: Attachment):
        return Attachment.model_validate({
            **db_attachment.model_dump(),
            "is_valid": False
        })

    return _factory
