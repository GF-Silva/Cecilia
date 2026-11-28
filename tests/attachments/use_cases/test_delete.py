from cecilia.use_cases import AttachmentDeleteUseCase, AttachmentShowPayload
from cecilia.models import AttachmentPublic

async def test_delete_success(mocker, attachment, attachment_invalid, chat, message):
    # Generarions
    gen_attachment = attachment()
    gen_chat = chat()
    gen_message = message(chat_id=gen_chat.id, is_user=True)

    # Mock
    mock_attachment_modify_facade = mocker.MagicMock()
    mock_attachment_modify_facade.return_value = gen_attachment

    mock_r2_integration = mocker.AsyncMock()
    mock_attachment_service = mocker.MagicMock()
    mock_attachment_service.invalidate.return_value = attachment_invalid(gen_attachment)

    # Instancing
    delete_use_case = AttachmentDeleteUseCase(
        attachment_modify_facade=mock_attachment_modify_facade,
        r2_integration=mock_r2_integration,
        attachments_service=mock_attachment_service
    )

    # Testing
    payload = AttachmentShowPayload(
        user_id=gen_chat.user_id,
        chat_id=gen_chat.id,
        message_id=gen_message.id,
        attachment_id=gen_attachment.id
    )
    result = await delete_use_case(payload)

    assert isinstance(result, AttachmentPublic)
    mock_attachment_service.invalidate.assert_called_once_with(id=gen_attachment.id, message_id=gen_message.id)
    mock_attachment_modify_facade.assert_called_once_with(
        chat_id=gen_chat.id,
        message_id=gen_message.id,
        user_id=gen_chat.user_id,
        attachment_id=gen_attachment.id
    )
    mock_r2_integration.delete_file.assert_called_once_with(path=gen_attachment.path)