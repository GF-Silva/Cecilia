from PIL import Image, UnidentifiedImageError
from io import BufferedIOBase
from typing import cast, BinaryIO
from .errors import FileError, InvalidFileError, FileTooBigError, EmptyFileError

# TODO: Add more validations using magic / file content / etc
class ImageValidator:
    def __call__(
        self,
        stream: BufferedIOBase
    ):
        stream.seek(0)

        if not stream.read(1):
            raise EmptyFileError()

        stream.seek(0)

        try:
            with Image.open(cast(BinaryIO, stream)) as img:
                img.verify()

        except UnidentifiedImageError:
            raise InvalidFileError()

        except Image.DecompressionBombError:
            raise FileTooBigError()

        except Exception as err:
            print("Attachments (CreateUseCase) - err: ", err)
            raise FileError()