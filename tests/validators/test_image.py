from cecilia.validators import ImageValidator
from cecilia.validators.errors import FileError
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

def test_fail(file):
    gen_file = next(file(
        mime_type='application/json',
        type='json'
    ))

    image_validator = ImageValidator()
    
    with pytest.raises(FileError):
        image_validator(gen_file.stream)
