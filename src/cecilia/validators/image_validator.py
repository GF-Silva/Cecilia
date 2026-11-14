from PIL import Image, UnidentifiedImageError
from typing import BinaryIO

from cecilia.core.exceptions import InvalidFileError, FileTooBigError, InternalError

# TODO: Add more validations using magic / file content / etc
class ImageValidator:    
    def __call__(
        self,
        stream: BinaryIO
    ): 
        try:
            stream.seek(0)
            with Image.open(stream) as img:
                img.verify()

        except UnidentifiedImageError:
            raise InvalidFileError()

        except Image.DecompressionBombError:
            raise FileTooBigError()

        except Exception as err:
            print("Attachments (CreateUseCase) - err: ", err)
            raise InternalError()