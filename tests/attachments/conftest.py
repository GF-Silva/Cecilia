import pytest
from tests.fakes.repositories import FakeAttachmentRepository
from cecilia.services import AttachmentService
from cecilia.models.tables import Attachment

@pytest.fixture
def fake_attachment_repo():
    return FakeAttachmentRepository()

@pytest.fixture
def attachment_service(fake_attachment_repo):
    return AttachmentService(attachment_repository=fake_attachment_repo)

@pytest.fixture
def attachment():
    return Attachment(id=1, mime_type='audio/mpeg', message_id=1)