from cecilia.core import exceptions
from cecilia.services import AttachmentService
import pytest

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