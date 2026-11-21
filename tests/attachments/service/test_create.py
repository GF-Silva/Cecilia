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

def test_create_rejects_create_to_message_not_found(mocker, attachment_create):
    # Generations
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
        attachment_service.create(attachment=gen_attachment_create, message_id=10)
    
    mock_message_repo.show.assert_called_once_with(id=10)
    mock_attachment_repo.create.assert_not_called()

def test_create_list_success(mocker, attachment_create, attachment, message):
    # Generations
    gen_message = message()
    gen_attachments = [
        attachment(id=1, message_id=gen_message.id),
        attachment(id=2, message_id=gen_message.id),
        attachment(id=3, message_id=gen_message.id)
    ]

    gen_attachments_create = [
        attachment_create(message_id=gen_message.id),
        attachment_create(message_id=gen_message.id),
        attachment_create(message_id=gen_message.id)
    ]

    # Mocks 
    mock_attachment_repo = mocker.MagicMock()
    mock_message_repo = mocker.MagicMock()

    # Return values
    mock_message_repo.show.return_value = gen_message
    mock_attachment_repo.create_list.return_value = gen_attachments

    # Creating instances
    attachment_service = AttachmentService(
        attachment_repository=mock_attachment_repo,
        message_repository=mock_message_repo
    )

    result = attachment_service.create_list(attachments=gen_attachments_create, message_id=gen_message.id)
    assert isinstance(result, list)
    assert all(isinstance(attachment, Attachment) for attachment in result)
    assert result == gen_attachments
    mock_message_repo.show.assert_called_once_with(id=gen_message.id)
    mock_attachment_repo.create_list.assert_called_once_with(gen_attachments_create)

def test_create_list_rejects_all_if_create_to_assistant_messages(mocker, attachment_create, message):
    # Generations
    gen_message = message(is_user=False)

    gen_attachments_create = [
        attachment_create(message_id=gen_message.id),
        attachment_create(message_id=gen_message.id),
        attachment_create(message_id=gen_message.id)
    ]

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
        attachment_service.create_list(attachments=gen_attachments_create, message_id=gen_message.id)
        
    mock_message_repo.show.assert_called_once_with(id=gen_message.id)
    mock_attachment_repo.create_list.assert_not_called()

def test_create_list_rejects_create_to_message_not_found(mocker, attachment_create, message):
    # Generations
    gen_attachments_create = [
        attachment_create(message_id=1),
        attachment_create(message_id=1),
        attachment_create(message_id=1)
    ]

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

    with pytest.raises(exceptions.RuleError):
        attachment_service.create_list(attachments=gen_attachments_create, message_id=1)
        
    mock_message_repo.show.assert_called_once_with(id=1)
    mock_attachment_repo.create_list.assert_not_called()