from cecilia.core import exceptions
from cecilia.services import AttachmentService
from cecilia.models.attachment_model import AttachmentUpdate
import pytest
from cecilia.models.tables import Attachment

@pytest.mark.parametrize(
    'is_user, should_work',
    [
        (False, False),
        (True, True)
    ]
)
def test_validate_message(mocker, message, is_user, should_work):
    mocker_repo = mocker.MagicMock()
    mock_message_repo = mocker.MagicMock()
    service = AttachmentService(attachment_repository=mocker_repo, message_repository=mock_message_repo)
    gen_message = message(is_user=is_user)

    if should_work:
        service.validate_message_role(gen_message)
    else:
        with pytest.raises(exceptions.RuleError):
            service.validate_message_role(gen_message)

def test_show_success(mocker, attachment):
    # Generations
    gen_attachment = attachment(id=1, message_id=1)

    # Mocks
    mock_attachment_repo = mocker.MagicMock()
    mock_message_repo = mocker.MagicMock()

    # Return values
    mock_attachment_repo.show.return_value = gen_attachment

    # Creating instances
    attachment_service = AttachmentService(
        attachment_repository=mock_attachment_repo,
        message_repository=mock_message_repo
    )

    result = attachment_service.show(message_id=gen_attachment.message_id, id=gen_attachment.id)
    assert result == gen_attachment
    mock_attachment_repo.show.assert_called_once_with(id=gen_attachment.id, message_id=gen_attachment.message_id)

def test_show_returns_not_found(mocker):
    # Mocks
    mock_attachment_repo = mocker.MagicMock()
    mock_message_repo = mocker.MagicMock()

    # Return values
    mock_attachment_repo.show.return_value = None

    # Creating instances
    attachment_service = AttachmentService(
        attachment_repository=mock_attachment_repo,
        message_repository=mock_message_repo
    
    )
    
    # Testing
    with pytest.raises(exceptions.NotFoundError):
        attachment_service.show(id=2, message_id=1)

    mock_attachment_repo.show.assert_called_once_with(id=2, message_id=1)

def test_delete_success(attachment_service, attachment):
    gen_attachment = attachment(id=1, message_id=1)
    attachment_service.attachment_repository.storage[gen_attachment.id] = gen_attachment
    attachment_service.delete(id=1, message_id=1)

def test_delete_error_not_found(attachment_service, attachment):
    gen_attachment = attachment(id=1, message_id=1)
    attachment_service.attachment_repository.storage[gen_attachment.id] = gen_attachment
    with pytest.raises(exceptions.NotFoundError):
        attachment_service.delete(id=2, message_id=1)

@pytest.mark.parametrize(
    'id, message_id, update_fields, should_work',
    [
        (1, 2, AttachmentUpdate(mime_type='test/test', message_id=10, is_valid=True), True),
        (10, 2, AttachmentUpdate(mime_type='test/test', message_id=10, is_valid=True), False)
    ]
)
def test_update(attachment_service, attachment, id, message_id, update_fields, should_work):
    gen_attachment = attachment(id=1, message_id=2)
    attachment_service.attachment_repository.storage[gen_attachment.id] = gen_attachment

    if should_work:
        updated_attachment = attachment_service.update(id=id, message_id=message_id, attachment_update=update_fields)
        assert updated_attachment.model_dump(include=update_fields.model_dump(exclude_unset=True)) == update_fields.model_dump(exclude_unset=True)
    else:
        with pytest.raises(exceptions.NotFoundError):
            attachment_service.update(id=id, message_id=message_id, attachment_update=update_fields)