from PIL import Image, UnidentifiedImageError
from typing import BinaryIO
from .errors import FileError, InvalidFileError, FileTooBigError, EmptyFileError

# TODO: Add more validations using magic / file content / etc
class ImageValidator:
    def __call__(
        self,
        stream: BinaryIO
    ):
        stream.seek(0)

        if not stream.read(1):
            raise EmptyFileError()

        stream.seek(0)

        try:
            with Image.open(stream) as img:
                img.verify()

        except UnidentifiedImageError:
            raise InvalidFileError()

        except Image.DecompressionBombError:
            raise FileTooBigError()

        except Exception as err:
            print("Attachments (CreateUseCase) - err: ", err)
            raise FileError()