from cecilia.core import exceptions
from cecilia.services import AttachmentService
from cecilia.models.attachment_model import AttachmentUpdate
import pytest

def test_delete_success(attachment, mocker):
    # Generations
    gen_attachment = attachment(id=1, message_id=1)

    # Mocks
    mock_message_repo = mocker.MagicMock()
    mock_attachment_repo = mocker.MagicMock()
    mock_attachment_repo.show.return_value=gen_attachment

    # Creating instances
    attachment_service = AttachmentService(
        message_repository=mock_message_repo,
        attachment_repository=mock_attachment_repo
    )

    # Testing
    attachment_service.delete(id=gen_attachment.id, message_id=gen_attachment.message_id)
    mock_attachment_repo.show.assert_called_once_with(id=gen_attachment.id, message_id=gen_attachment.message_id)
    mock_attachment_repo.delete.assert_called_once_with(gen_attachment)

def test_delete_error_not_found(attachment_service, attachment):
    gen_attachment = attachment(id=1, message_id=1)
    attachment_service.attachment_repository.storage[gen_attachment.id] = gen_attachment
    with pytest.raises(exceptions.NotFoundError):
        attachment_service.delete(id=2, message_id=1)
