from cecilia.use_cases import AttachmentShowUseCase, AttachmentShowPayload
from cecilia.models import AttachmentPublic

def test_access_success(mocker, attachment, chat, message):
    # Generarions
    gen_attachment = attachment()
    gen_attachment_public = AttachmentPublic.model_validate(gen_attachment.model_dump())
    gen_chat = chat()
    gen_message = message(chat_id=gen_chat.id, is_user=True)

    # Mock
    mock_attachment_show_facade = mocker.MagicMock()
    mock_attachment_show_facade.return_value = gen_attachment

    # Instancing
    show_use_case = AttachmentShowUseCase(attachment_show_facade=mock_attachment_show_facade)

    # Testing
    payload = AttachmentShowPayload(
        user_id=gen_chat.user_id,
        chat_id=gen_chat.id,
        message_id=gen_message.id,
        attachment_id=1
    )
    result = show_use_case(payload)

    assert result == gen_attachment_public
    assert isinstance(result, AttachmentPublic)
    mock_attachment_show_facade.assert_called_once_with(
        chat_id=gen_chat.id,
        message_id=gen_message.id,
        user_id=gen_chat.user_id,
        attachment_id=1
    )