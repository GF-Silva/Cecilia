from cecilia.use_cases import AttachmentCreateUseCase, AttachmentCreatePayload
from cecilia.models import AttachmentPublic
from cecilia.extractors import FileMetadata

async def test_create_acceps_single_file(mocker, chat, message, attachment, file):
    # Configs | Gens
    user_id=1
    gen_chat=chat()
    gen_message=message()

    gen_file = next(file(
        mime_type='audio/mpeg',
        type='mp3'
    ))

    # Mocks
    mock_create_facade = mocker.MagicMock()
    mock_file_metada_extractor = mocker.MagicMock()
    mock_validation_policy_dispatcher = mocker.MagicMock()
    mock_service = mocker.MagicMock()
    mock_r2_integration = mocker.AsyncMock()

    mock_service.create.return_value = attachment()
    mock_file_metada_extractor.return_value = FileMetadata(
        mime_type=gen_file.mime_type,
        size=gen_file.size
    )

    # Instances
    create_use_case = AttachmentCreateUseCase(
        create_facade=mock_create_facade,
        file_metada_extractor=mock_file_metada_extractor,
        validation_policy_dispatcher=mock_validation_policy_dispatcher,
        service=mock_service,
        r2_integration=mock_r2_integration
    )

    # Testing
    result = await create_use_case(payload=AttachmentCreatePayload(
        user_id=user_id,
        chat_id=gen_chat.id,
        message_id=gen_message.id,
        file=gen_file.stream,
        filename=gen_file.filename
    ))

    assert isinstance(result, AttachmentPublic)
    mock_create_facade.assert_called_once_with(
        user_id=user_id,
        chat_id=gen_chat.id,
        message_id=gen_message.id
    )

    mock_file_metada_extractor.assert_called_once_with(file=gen_file.stream)
    mock_validation_policy_dispatcher.assert_called_once_with(
        mime_type=gen_file.mime_type,
        file=gen_file.stream,
        size=gen_file.size
    )
    mock_service.create.assert_called_once()
    mock_r2_integration.create_file.assert_called_once()