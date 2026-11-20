from cecilia.models.tables import Message, Attachment
from cecilia.core import exceptions
from cecilia.services import AttachmentService
import uuid
import pytest

def test_validate_message_role_rejects_assistant(mocker):
    mocker_repo = mocker.MagicMock()
    service = AttachmentService(attachment_repository=mocker_repo)
    message = Message(chat_id=uuid.uuid7(), is_user=False)

    with pytest.raises(exceptions.RuleError):
        service.validate_message_role(message)

def test_validate_message_role_accepts_user(mocker):
    mocker_repo = mocker.MagicMock()
    service = AttachmentService(attachment_repository=mocker_repo)
    message = Message(chat_id=uuid.uuid7(), is_user=True)
    service.validate_message_role(message)

def test_show_success(attachment_service, attachment):
    attachment_service.attachment_repository.storage[attachment.id] = attachment
    result = attachment_service.show(message_id=attachment.message_id, id=attachment.id)
    assert result == attachment

def test_show_returns_not_found(attachment_service, attachment):
    attachment_service.attachment_repository.storage[attachment.id] = attachment
    
    with pytest.raises(exceptions.NotFoundError):
        attachment_service.show(id=2, message_id=1)