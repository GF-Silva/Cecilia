import pytest
from cecilia.use_cases import AttachmentCreateUseCase, AttachmentCreatePayload
from cecilia.extractors import FileMetadata

async def test_create_acceps_single_file(mocker, chat, message, file):
    # Configs | Gens
    user_id=1
    gen_chat=chat()
    gen_message=message() # TODO: Attachment configs here

    gen_file = next(file(
        mime_type='audio/mpeg',
        type='mp3'
    ))

    # Mocks
    mock_create_facade = mocker.MagicMock()
    mock_file_metada_extractor = mocker.MagicMock()
    mock_validation_policy_dispatcher = mocker.MagicMock()
    mock_service = mocker.MagicMock()
    mock_r2_integration = mocker.MagicMock()

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
    create_use_case(payload=AttachmentCreatePayload(
        user_id=user_id,
        chat_id=gen_chat.id,
        message_id=gen_message.id,
        file=gen_file.stream
    ))
