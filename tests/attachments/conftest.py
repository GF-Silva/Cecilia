import pytest
from tests.fakes.repositories import FakeAttachmentRepository
from cecilia.services import AttachmentService
from cecilia.models.tables import Attachment
import uuid
from datetime import datetime, UTC

@pytest.fixture
def fake_attachment_repo():
    return FakeAttachmentRepository()

@pytest.fixture
def attachment_service(fake_attachment_repo):
    return AttachmentService(attachment_repository=fake_attachment_repo)

@pytest.fixture
def attachment():
    def _factory(
        mime_type: str = 'audio/mpeg',
        message_id: int = 1,
        size: int | None = None,
        filename: uuid.UUID | None = None,
        public_filename: str | None = None,
        is_valid: bool | None = None,
        created_at: datetime | None = None,
        id: int = 1
    ):
        return Attachment(
            mime_type=mime_type, 
            message_id=message_id, 
            size=size, 
            filename=filename if filename is not None else uuid.uuid7(),
            public_filename=public_filename,
            is_valid=is_valid,
            created_at=created_at if created_at is not None else datetime.now(UTC),
            id=id
        )
    
    return _factory