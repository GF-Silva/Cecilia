from PIL import Image, UnidentifiedImageError
from typing import BinaryIO

from cecilia.core.exceptions import InvalidFileError, FileTooBigError, InternalError
from .errors import EmptyFileError, InvalidFileType
import magic

# TODO: Add more validations using magic / file content / etc
class ImageValidator:
    MIME_VALIDATOR = magic.Magic(mime=True) # TODO: Reuse the same

    def __call__(
        self,
        stream: BinaryIO
    ): 
        stream.seek(0)
        data = stream.read()

        if not data:
            raise EmptyFileError()

        mime_type = self.MIME_VALIDATOR.from_buffer(data)

        if not mime_type.startswith('image/'):
            raise InvalidFileType(message='The file is not an image')
        
        try:
            with Image.open(stream) as img:
                img.verify()

        except UnidentifiedImageError:
            raise InvalidFileError()

        except Image.DecompressionBombError:
            raise FileTooBigError()

        except Exception as err:
            print("Attachments (CreateUseCase) - err: ", err)
            raise InternalError()