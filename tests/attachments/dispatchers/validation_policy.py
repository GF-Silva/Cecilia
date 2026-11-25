from cecilia.dispatchers import AttachmentValidationPolicyDispatcher
from cecilia.dispatchers.attachments.errors import UnsupportedFileFormatError
import pytest

def test_dispatch_accepts_audio(mocker, file):
    mock_attachment_image_validation_policy = mocker.MagicMock()
    mock_attachment_audio_validation_policy = mocker.MagicMock()
    gen_file = file(
        mime_type='audio/mpeg',
        type='mp3'
    )

    dispatcher = AttachmentValidationPolicyDispatcher(
        attachment_image_validation_policy=mock_attachment_image_validation_policy,
        attachment_audio_validation_policy=mock_attachment_audio_validation_policy
    )

    dispatcher(mime_type='audio/mpeg', file=gen_file)
    mock_attachment_audio_validation_policy.assert_called_once_with(file=gen_file)
    mock_attachment_image_validation_policy.assert_not_called()

def test_dispatch_accepts_image(mocker, file):
    mock_attachment_image_validation_policy = mocker.MagicMock()
    mock_attachment_audio_validation_policy = mocker.MagicMock()
    gen_file = file(
        mime_type='image/png',
        type='png'
    )

    dispatcher = AttachmentValidationPolicyDispatcher(
        attachment_image_validation_policy=mock_attachment_image_validation_policy,
        attachment_audio_validation_policy=mock_attachment_audio_validation_policy
    )

    dispatcher(mime_type='image/png', file=gen_file)
    mock_attachment_audio_validation_policy.assert_not_called()
    mock_attachment_image_validation_policy.assert_called_once_with(file=gen_file)
