from cecilia.core import exceptions
from cecilia.services import AttachmentService
import uuid
import pytest

def test_validate_message_role_rejects_assistant(mocker, message):
    mocker_repo = mocker.MagicMock()
    service = AttachmentService(attachment_repository=mocker_repo)
    gen_message = message(is_user=False)

    with pytest.raises(exceptions.RuleError):
        service.validate_message_role(gen_message)

def test_validate_message_role_accepts_user(mocker, message):
    mocker_repo = mocker.MagicMock()
    service = AttachmentService(attachment_repository=mocker_repo)
    gen_message = message(is_user=True)
    service.validate_message_role(gen_message)

def test_show_success(attachment_service, attachment):
    gen_attachment = attachment(id=1, message_id=1)
    attachment_service.attachment_repository.storage[gen_attachment.id] = gen_attachment
    result = attachment_service.show(message_id=gen_attachment.message_id, id=gen_attachment.id)
    assert result == gen_attachment

def test_show_returns_not_found(attachment_service, attachment):
    gen_attachment = attachment(id=1, message_id=1)
    attachment_service.attachment_repository.storage[gen_attachment.id] = gen_attachment
    
    with pytest.raises(exceptions.NotFoundError):
        attachment_service.show(id=2, message_id=1)