import pytest
from cecilia.use_cases import DeleteAttachmentUseCase
from cecilia.models.attachment_model import AttachmentUpdate
from cecilia.models.tables import Attachment

async def test_delete_use_case(mocker, attachment):
    gen_attachment = attachment(id=1, message_id=1, is_valid=None)
    mock_r2_integration = mocker.AsyncMock()
    mock_attachments_service = mocker.Mock()
    mock_attachments_service.update.return_value = Attachment.model_validate({
        **gen_attachment.model_dump(), 
        "is_valid": False
    })

    use_case = DeleteAttachmentUseCase(
        r2_integration=mock_r2_integration, 
        attachments_service=mock_attachments_service
    )

    await use_case(attachment_id=gen_attachment.id, message_id=gen_attachment.message_id)

    mock_attachments_service.update.assert_called_once_with(
        id=gen_attachment.id,
        message_id=gen_attachment.message_id,
        attachment_update=AttachmentUpdate(is_valid=False)
    )
    mock_r2_integration.delete_file.assert_called_once_with(gen_attachment.path)

    # TODO: Finish the features requests based on Test-Driven-Development