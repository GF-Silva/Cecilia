from cecilia.core import exceptions
from cecilia.services import AttachmentService
import pytest
from cecilia.models.tables import Attachment

def test_create_success(mocker, attachment_create, attachment, message):
    # Generations
    gen_attachment = attachment(id=1, message_id=1)
    gen_message = message()
    gen_attachment_create = attachment_create()

    # Mocks
    mock_attachment_repo = mocker.MagicMock()
    mock_message_repo = mocker.MagicMock()

    # Return values
    mock_message_repo.show.return_value = gen_message
    mock_attachment_repo.create.return_value = gen_attachment

    # Creating instances
    attachment_service = AttachmentService(
        attachment_repository=mock_attachment_repo,
        message_repository=mock_message_repo
    )

    result = attachment_service.create(attachment=gen_attachment_create, message_id=gen_message.id)
    assert isinstance(result, Attachment)
    assert result == gen_attachment
    mock_message_repo.show.assert_called_once_with(id=gen_attachment.message_id)
    mock_attachment_repo.create.assert_called_once_with(gen_attachment_create)

def test_create_rejects_create_to_assistant_messages(mocker, attachment_create, attachment, message):
    # Generations
    gen_attachment = attachment(id=1, message_id=1)
    gen_message = message(is_user=False)
    gen_attachment_create = attachment_create()

    # Mocks
    mock_attachment_repo = mocker.MagicMock()
    mock_message_repo = mocker.MagicMock()

    # Return values
    mock_message_repo.show.return_value = gen_message

    # Creating instances
    attachment_service = AttachmentService(
        attachment_repository=mock_attachment_repo,
        message_repository=mock_message_repo
    )

    with pytest.raises(exceptions.RuleError):
        attachment_service.create(attachment=gen_attachment_create, message_id=gen_message.id)
    
    mock_message_repo.show.assert_called_once_with(id=gen_attachment.message_id)
    mock_attachment_repo.create.assert_not_called()

def test_create_rejects_create_to_messages_not_found(mocker, attachment, message, attachment_create):
    # Generations
    gen_attachment = attachment(id=1, message_id=1)
    gen_message = message(is_user=True)
    gen_attachment_create = attachment_create()

    # Mocks
    mock_attachment_repo = mocker.MagicMock()
    mock_message_repo = mocker.MagicMock()

    # Return values
    mock_message_repo.show.return_value = None

    # Creating instances
    attachment_service = AttachmentService(
        attachment_repository=mock_attachment_repo,
        message_repository=mock_message_repo
    )

    # Tests
    with pytest.raises(exceptions.RuleError):
        attachment_service.create(attachment=gen_attachment_create, message_id=gen_message.id)
    
    mock_message_repo.show.assert_called_once_with(id=gen_attachment.message_id)
    mock_attachment_repo.create.assert_not_called()

@pytest.mark.parametrize(
    'is_user, should_work',
    [
        (True, True),
        (False, False)
    ]
)
def test_create_list(attachment_create, attachment_service, message, is_user, should_work):
    gen_message = message(is_user=is_user)
    attachment_service.message_repository.show.return_value = gen_message

    attachments = [
        attachment_create(),
        attachment_create(),
        attachment_create()
    ]

    if should_work:
        attachment_service.create_list(attachments=attachments, message_id=gen_message.id)
    else:
        with pytest.raises(exceptions.RuleError):
            attachment_service.create_list(attachments=attachments, message_id=gen_message.id)
