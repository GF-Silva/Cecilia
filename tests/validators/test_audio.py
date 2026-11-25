from cecilia.validators import AudioValidator
from cecilia.validators.errors import EmptyFileError, InvalidFileError
from typing import BinaryIO
import pytest

async def test_success(mocker, file):
    gen_file = next(file(
        mime_type='audio/mpeg',
        type='mp3'
    ))

    mock_ffprobe_adapter = mocker.AsyncMock()
    audio_validator = AudioValidator(ffprobe_adapter=mock_ffprobe_adapter)
    await audio_validator(stream=gen_file.stream)
    mock_ffprobe_adapter.validate_file_from_buffer.assert_called_once()

async def test_rejecs_empty_file(mocker):
    gen_file = BinaryIO()

    mock_ffprobe_adapter = mocker.AsyncMock()
    audio_validator = AudioValidator(ffprobe_adapter=mock_ffprobe_adapter)

    with pytest.raises(EmptyFileError):
        await audio_validator(stream=gen_file)
    
    mock_ffprobe_adapter.validate_file_from_buffer.assert_not_called()

async def test_rejecs_invalid_file(mocker, file):
    gen_file = next(file(
        mime_type='audio/mpeg',
        type='mp3',
        filename='file_invalid'
    ))

    mock_ffprobe_adapter = mocker.AsyncMock()
    mock_ffprobe_adapter.validate_file_from_buffer.side_effect = InvalidFileError()
    audio_validator = AudioValidator(ffprobe_adapter=mock_ffprobe_adapter)

    with pytest.raises(InvalidFileError):
        await audio_validator(stream=gen_file.stream)
    
    mock_ffprobe_adapter.validate_file_from_buffer.assert_called_once()
