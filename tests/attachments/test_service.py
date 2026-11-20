from cecilia.models.tables import Message
from cecilia.core.exceptions import RuleError
from cecilia.services import AttachmentService
import uuid
import pytest

def test_validate_message_role_rejects_assistant(mocker):
    mocker_repo = mocker.MagicMock()
    service = AttachmentService(attachment_repository=mocker_repo)
    message = Message(chat_id=uuid.uuid7(), is_user=False)

    with pytest.raises(RuleError):
        service.validate_message_role(message)

def test_validate_message_role_accepts_user(mocker):
    mocker_repo = mocker.MagicMock()
    service = AttachmentService(attachment_repository=mocker_repo)
    message = Message(chat_id=uuid.uuid7(), is_user=True)
    service.validate_message_role(message)