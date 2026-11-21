import pytest
from cecilia.use_cases import DeleteAttachmentUseCase, CreateAttachmentsUseCase
from cecilia.models.attachment_model import AttachmentUpdate
from cecilia.models.tables import Attachment
from fastapi import UploadFile
from cecilia.validators.responses import FileData
from cecilia.core.exceptions import RuleError, SimulatedError

async def test_delete(mocker, attachment):
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

async def test_create_accepts_single_file(mocker, message, file):
    # Generations
    gen_message = message(is_user=True)
    gen_file = next(file(mime_type='audio/mpeg', type='mp3'))

    # Mock
    mock_attachment_service = mocker.MagicMock()
    mock_r2_integration = mocker.AsyncMock()
    mock_file_validator = mocker.AsyncMock()

    # Return values
    mock_file_validator.return_value = FileData(
        stream=gen_file.stream,
        mime_type=gen_file.mime_type,
        size=gen_file.size
    )

    # Creating instances
    create_attachments_use_case = CreateAttachmentsUseCase(
        attachment_service=mock_attachment_service,
        r2_integration=mock_r2_integration,
        file_validator=mock_file_validator
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
    mock_file_validator.assert_called_once()

async def test_create_accepts_multiple_files(mocker, message, file):
    # Mock
    mock_attachment_service = mocker.MagicMock()
    mock_r2_integration = mocker.AsyncMock()
    mock_file_validator = mocker.AsyncMock()

    # Generations
    gen_message = message(is_user=True)
    gen_files = [
        next(file(mime_type='audio/mpeg', type='mp3')),
        next(file(mime_type='image/png', type='png')),
        next(file(mime_type='image/jpeg', type='jpg'))
    ]

    mock_file_validator.side_effect = [
        FileData(
            stream=gen_file.stream,
            mime_type=gen_file.mime_type,
            size=gen_file.size
        ) for gen_file in gen_files
    ]

    # Creating instances
    create_attachments_use_case = CreateAttachmentsUseCase(
        attachment_service=mock_attachment_service,
        r2_integration=mock_r2_integration,
        file_validator=mock_file_validator
    )

    await create_attachments_use_case(
        message_id=1,
        message=gen_message,
        files=[UploadFile(gen_file.stream) for gen_file in gen_files]
    )

    # Assertions
    mock_r2_integration.create_file.assert_called()
    assert mock_r2_integration.create_file.call_count == len(gen_files)
    mock_attachment_service.create_list.assert_called_once()
    mock_file_validator.assert_called()
    assert mock_file_validator.call_count == len(gen_files)
    mock_attachment_service.validate_message_role.assert_called_once_with(gen_message)

async def test_create_rejects_assistant_messages(mocker, message, file):
    # Mock
    mock_attachment_service = mocker.MagicMock()
    mock_r2_integration = mocker.AsyncMock()
    mock_file_validator = mocker.AsyncMock()

    # Returns | Side effects set
    mock_file_validator.side_effect = SimulatedError()
    mock_attachment_service.validate_message_role.side_effect = SimulatedError()

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
    with pytest.raises(SimulatedError):
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

async def test_create_rejects_invalid_files(mocker, message, file):
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
    mock_file_validator.side_effect = SimulatedError()

    with pytest.raises(SimulatedError):
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

# TODO: The creation should skip invalid files and return when some error happens
async def test_create_rejects_all_if_invalid_files(mocker, message, file):
    # Mock
    mock_attachment_service = mocker.MagicMock()
    mock_r2_integration = mocker.AsyncMock()
    mock_file_validator = mocker.AsyncMock()

    # Generations
    gen_message = message(is_user=True)
    gen_files = [
        next(file(mime_type='audio/mpeg', type='mp3')),
        next(file(mime_type='application/json', type='json')),
        next(file(mime_type='image/jpeg', type='jpg'))
    ]

    mock_file_validator.side_effect = [
        gen_files[0],
        SimulatedError(),
        gen_files[2]
    ]

    # Creating instances
    create_attachments_use_case = CreateAttachmentsUseCase(
        attachment_service=mock_attachment_service,
        r2_integration=mock_r2_integration,
        file_validator=mock_file_validator
    )

    with pytest.raises(SimulatedError):
        await create_attachments_use_case(
            message_id=1,
            message=gen_message,
            files=[UploadFile(gen_file.stream) for gen_file in gen_files]
        )

    # Assertions
    mock_file_validator.assert_called()
    assert mock_file_validator.call_count == 2
    mock_attachment_service.validate_message_role.assert_called_once_with(gen_message)
    mock_r2_integration.create_file.assert_not_called()
    mock_attachment_service.create_list.assert_not_called()

@pytest.mark.parametrize(
    'type',
    [
        (True),
        ([]),
        (None),
        ([None]),
        (1),
        ("String")
    ]
)
async def test_create_rejects_input_types_different_from_expected(mocker, message, type):
    # Mock
    mock_attachment_service = mocker.MagicMock()
    mock_r2_integration = mocker.AsyncMock()
    mock_file_validator = mocker.AsyncMock()

    # Creating instances
    # TODO: Criar uma fixture disso
    create_attachments_use_case = CreateAttachmentsUseCase(
        attachment_service=mock_attachment_service,
        r2_integration=mock_r2_integration,
        file_validator=mock_file_validator
    )

    with pytest.raises(RuleError):
        await create_attachments_use_case(
            message_id=1,
            message=message(is_user=True),
            files=type
        )

    # Assertions
    mock_attachment_service.validate_message_role.assert_not_called()
    mock_file_validator.assert_not_called()
    mock_attachment_service.create_list.assert_not_called()
    mock_r2_integration.create_file.assert_not_called()

# TODO: Check if create file accepts upload types different from BinaryIO | UploadFile
# TODO: Check if the file sent is valid