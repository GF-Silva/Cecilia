from cecilia.core import exceptions
from cecilia.services import AttachmentService
from cecilia.models.attachment_model import AttachmentUpdate
import pytest

def test_delete_success(attachment_service, attachment):
    gen_attachment = attachment(id=1, message_id=1)
    attachment_service.attachment_repository.storage[gen_attachment.id] = gen_attachment
    attachment_service.delete(id=1, message_id=1)

def test_delete_error_not_found(attachment_service, attachment):
    gen_attachment = attachment(id=1, message_id=1)
    attachment_service.attachment_repository.storage[gen_attachment.id] = gen_attachment
    with pytest.raises(exceptions.NotFoundError):
        attachment_service.delete(id=2, message_id=1)
