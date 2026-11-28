from cecilia.use_cases import AttachmentCreatePayload, File
from cecilia.models import AttachmentPublic

async def test_create_accepts_file_list(mocker, attachment_create_use_case):
    # Configs | Gens
    create_use_case_fixture = attachment_create_use_case()

    # Testing
    result = await create_use_case_fixture.create_use_case(payload=AttachmentCreatePayload(
        user_id=create_use_case_fixture.user_id,
        chat_id=create_use_case_fixture.gen_chat.id,
        message_id=create_use_case_fixture.gen_message.id,
        files=[File(stream=file.stream, filename=file.public_filename) for file in create_use_case_fixture.gen_files]
    ))

    assert isinstance(result, list)
    for i in result:
        assert isinstance(i, AttachmentPublic)
    
    create_use_case_fixture.create_facade.assert_called_once_with(
        user_id=create_use_case_fixture.user_id,
        chat_id=create_use_case_fixture.gen_chat.id,
        message_id=create_use_case_fixture.gen_message.id
    )

    create_use_case_fixture.file_metada_extractor.assert_has_calls([
        mocker.call(file=file.stream) 
        for file in create_use_case_fixture.gen_files
    ])
    create_use_case_fixture.validation_policy_dispatcher.assert_has_calls(
        mocker.call(
            mime_type=gen_file.mime_type,
            file=gen_file.stream,
            size=gen_file.size
        ) for gen_file in create_use_case_fixture.gen_files
    )
    create_use_case_fixture.service.create_list.assert_called_once()
    create_use_case_fixture.r2_integration.create_file.assert_called()
