from cecilia.use_cases import AttachmentCreateUseCase, AttachmentCreatePayload, File
from cecilia.models import AttachmentPublic
from cecilia.extractors import FileMetadata

async def test_create_accepts_file_list(mocker, chat, message, attachment, file):
    # Configs | Gens
    user_id=1
    gen_chat=chat()
    gen_message=message()

    valid_files = [
        next(file(
            mime_type='audio/mpeg',
            type='mp3'
        )),
        next(file(
            mime_type='audio/mpeg',
            type='mp3'
        )),
        next(file(
            mime_type='audio/mpeg',
            type='mp3'
        ))
    ]
    invalid_files = []
    gen_files = [
        file for file in valid_files + invalid_files
    ]

    # Mocks
    mock_create_facade = mocker.MagicMock()
    mock_file_metada_extractor = mocker.MagicMock()
    mock_validation_policy_dispatcher = mocker.MagicMock()
    mock_service = mocker.MagicMock()
    mock_r2_integration = mocker.AsyncMock()

    mock_service.create_list.return_value = [
        attachment(
            id=id,
            mime_type=file.mime_type, 
            size=file.size, 
            message_id=gen_message.id, 
            public_filename=file.public_filename, 
            is_valid=True
        ) for id, file in enumerate(gen_files, 1)
    ]

    mock_file_metada_extractor.side_effect = [
        FileMetadata(
            mime_type=gen_file.mime_type,
            size=gen_file.size
        ) for gen_file in gen_files
    ]

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
        files=[File(stream=file.stream, filename=file.public_filename) for file in gen_files]
    ))

    assert isinstance(result, list)
    for i in result:
        assert isinstance(i, AttachmentPublic)
    
    mock_create_facade.assert_called_once_with(
        user_id=user_id,
        chat_id=gen_chat.id,
        message_id=gen_message.id
    )

    mock_file_metada_extractor.assert_has_calls([mocker.call(file=file.stream) for file in gen_files])
    mock_validation_policy_dispatcher.assert_has_calls(
        mocker.call(mime_type=gen_file.mime_type,
        file=gen_file.stream,
        size=gen_file.size)
        for gen_file in gen_files
    )
    mock_service.create_list.assert_called_once()
    mock_r2_integration.create_file.assert_called()

    assert mock_file_metada_extractor.call_count == len(gen_files)
    assert mock_validation_policy_dispatcher.call_count == len(gen_files)
    assert mock_r2_integration.create_file.call_count == len(valid_files)