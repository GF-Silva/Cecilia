import pytest
from cecilia.use_cases import DeleteAttachmentUseCase, CreateAttachmentsUseCase
from cecilia.models.attachment_model import AttachmentUpdate
from cecilia.models.tables import Attachment
from fastapi import UploadFile
from cecilia.validators.responses import FileData
from cecilia.validators.errors import FileError

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

# TODO? : Validate multi attachments
async def test_create_use_case_success(mocker, message, file):
    # Mock
    mock_attachment_service = mocker.MagicMock()
    mock_r2_integration = mocker.AsyncMock()
    mock_file_validator = mocker.AsyncMock()

    # Generations
    gen_message = message(is_user=True)
    gen_file = next(file(mime_type='audio/mpeg', type='mp3'))

    # Creating instances
    create_attachments_use_case = CreateAttachmentsUseCase(
        attachment_service=mock_attachment_service,
        r2_integration=mock_r2_integration,
        file_validator=mock_file_validator
    )

    mock_file_validator.return_value = FileData(
        stream=gen_file.stream,
        mime_type=gen_file.mime_type,
        size=gen_file.size
    )

    await create_attachments_use_case(
        message_id=1,
        message=gen_message,
        files=[UploadFile(gen_file.stream)]
    )

    # Assertions
    mock_r2_integration.create_file.assert_called_once()
    mock_attachment_service.create_list.assert_called_once()
    mock_attachment_service.validate_message_role.assert_called_once_with(gen_message)

async def test_create_use_case_rejects_assistant_messages(mocker, message, file):
    # Mock
    mock_attachment_service = mocker.MagicMock()
    mock_r2_integration = mocker.AsyncMock()
    mock_file_validator = mocker.AsyncMock()

    # Returns | Side effects set
    mock_file_validator.side_effect = FileError('Erro simulado') # TODO: Substituir por SimulatedError
    mock_attachment_service.validate_message_role.side_effect = FileError('Erro simulado')

    # Generations
    gen_message = message(is_user=False)
    gen_file = next(file(
        mime_type='audio/mpeg',
        type='mp3'
    ))

    # Creating instances
    create_attachments_use_case = CreateAttachmentsUseCase(
        attachment_service=mock_attachment_service,
        r2_integration=mock_r2_integration,
        file_validator=mock_file_validator
    )

    # Testing
    with pytest.raises(FileError):
        await create_attachments_use_case(
            message_id=1,
            message=gen_message,
            files=[UploadFile(gen_file.stream)]
        )

    # Assertions
    mock_attachment_service.validate_message_role.assert_called_once_with(gen_message)    
    mock_file_validator.assert_not_called()
    mock_r2_integration.create_file.assert_not_called()
    mock_attachment_service.create_list.assert_not_called()

async def test_create_use_case_refuses_unsupported_files(mocker, message, file):
    # Mock
    mock_attachment_service = mocker.MagicMock()
    mock_r2_integration = mocker.AsyncMock()
    mock_file_validator = mocker.AsyncMock()

    # Generations
    gen_message = message(is_user=True)
    gen_file = next(file(
        mime_type='application/json',
        type='json'
    ))

    # Creating instances
    create_attachments_use_case = CreateAttachmentsUseCase(
        attachment_service=mock_attachment_service,
        r2_integration=mock_r2_integration,
        file_validator=mock_file_validator
    )

    mock_file_validator.side_effect = FileError('Erro simulado')

    with pytest.raises(FileError):
        await create_attachments_use_case(
            message_id=1,
            message=gen_message,
            files=[UploadFile(gen_file.stream)]
        )

    # Assertions
    mock_attachment_service.validate_message_role.assert_called_once_with(gen_message)
    mock_file_validator.assert_called_once()
    mock_attachment_service.create_list.assert_not_called()
    mock_r2_integration.create_file.assert_not_called()