from PIL import Image, UnidentifiedImageError
from typing import BinaryIO

from cecilia.services import AttachmentService
from cecilia.core.exceptions import InvalidFileError, FileTooBigError, InternalError

class ImageValidator:    
    def __init__(
        self,
        attachment_service: AttachmentService
    ):
        self.attachment_service = attachment_service

    def __call__(
        self,
        stream: BinaryIO
    ): 
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