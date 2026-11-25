from cecilia.policies import AttachmentImageValidationPolicy
from cecilia.policies.validators import FileTooBigError
from cecilia.core.exceptions import SimulatedError
import pytest

async def test_success(file, mocker):
    gen_file = next(file(
        mime_type='image/png',
        type='png'
    ))

    mock_image_validator = mocker.MagicMock()

    image_validation_policy = AttachmentImageValidationPolicy(image_validator=mock_image_validator)
    image_validation_policy(file=gen_file.stream, size=20_000_000)

    mock_image_validator.assert_called_once()

async def test_refuses_files_bigger_than_20_mb(file, mocker):
    gen_file = next(file(
        mime_type='image/png',
        type='png'
    ))

    mock_image_validator = mocker.MagicMock()

    with pytest.raises(FileTooBigError):
        image_validation_policy = AttachmentImageValidationPolicy(image_validator=mock_image_validator)
        image_validation_policy(file=gen_file.stream, size=20_000_001)

    mock_image_validator.assert_not_called()

async def test_refuses_invalid_files(file, mocker):
    gen_file = next(file(
        mime_type='image/png',
        type='png'
    ))

    mock_image_validator = mocker.MagicMock()
    mock_image_validator.side_effect = SimulatedError()

    with pytest.raises(SimulatedError):
        image_validation_policy = AttachmentImageValidationPolicy(image_validator=mock_image_validator)
        image_validation_policy(file=gen_file.stream, size=20_000_000)

    mock_image_validator.assert_called_once_with(stream=gen_file.stream)
