from cecilia.validators import ImageValidator
import pytest

@pytest.mark.parametrize(
    'mime_type, type, filename',
    [
        ('image/jpeg', 'jpg', 'file1'),
        ('image/jpeg', 'jpg', 'file2'),
        ('image/jpeg', 'jpg', 'file3'),
        ('image/png', 'png', 'file1')
    ]
)
def test_success(file, mime_type, type, filename):
    gen_file = next(file(
        mime_type=mime_type,
        type=type,
        filename=filename
    ))

    image_validator = ImageValidator()
    image_validator(gen_file.stream)
