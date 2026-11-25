from cecilia.policies import AttachmentAudioValidationPolicy
from cecilia.policies.validators import FileTooBigError
from cecilia.core.exceptions import SimulatedError
import pytest

async def test_success(file, mocker):
    gen_file = next(file(
        mime_type='audio/mpeg',
        type='mp3'
    ))

    mock_audio_validator = mocker.AsyncMock()

    audio_validation_policy = AttachmentAudioValidationPolicy(audio_validator=mock_audio_validator)
    await audio_validation_policy(file=gen_file.stream, size=100_000_000)

    mock_audio_validator.assert_called_once()

async def test_refuses_files_bigger_than_100_mb(file, mocker):
    gen_file = next(file(
        mime_type='audio/mpeg',
        type='mp3'
    ))

    mock_audio_validator = mocker.AsyncMock()

    with pytest.raises(FileTooBigError):
        audio_validation_policy = AttachmentAudioValidationPolicy(audio_validator=mock_audio_validator)
        await audio_validation_policy(file=gen_file.stream, size=100_000_001)

    mock_audio_validator.assert_not_called()

async def test_refuses_invalid_files(file, mocker):
    gen_file = next(file(
        mime_type='audio/mpeg',
        type='mp3'
    ))

    mock_audio_validator = mocker.AsyncMock()
    mock_audio_validator.side_effect = SimulatedError()
    audio_validation_policy = AttachmentAudioValidationPolicy(audio_validator=mock_audio_validator)

    with pytest.raises(SimulatedError):
        await audio_validation_policy(file=gen_file.stream, size=100_000_000)

    mock_audio_validator.assert_called_once_with(stream=gen_file.stream)
