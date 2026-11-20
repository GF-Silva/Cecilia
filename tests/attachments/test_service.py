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
    gen_attch = attachment(id=1, message_id=1)
    attachment_service.attachment_repository.storage[gen_attch.id] = gen_attch
    result = attachment_service.show(message_id=gen_attch.message_id, id=gen_attch.id)
    assert result == gen_attch

def test_show_returns_not_found(attachment_service, attachment):
    gen_atach = attachment(id=1, message_id=1)
    attachment_service.attachment_repository.storage[gen_atach.id] = gen_atach
    
    with pytest.raises(exceptions.NotFoundError):
        attachment_service.show(id=2, message_id=1)