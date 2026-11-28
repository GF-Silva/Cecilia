from io import BufferedIOBase
import asyncio
import magic
from .audio_validator import AudioValidator
from .image_validator import ImageValidator
from .errors import EmptyFileError
from .responses import FileData
from cecilia.core.exceptions import UnsupportedFileFormatError, FileTooBigError

class FileValidator:
    MIME_VALIDATOR = magic.Magic(mime=True)

    def __init__(
        self,
        image_validator: ImageValidator,
        audio_validator: AudioValidator
    ):
        self.image_validator = image_validator
        self.audio_validator = audio_validator

    # TODO: Paralelismo com asyncio.gather e to_thread
    async def __call__(
        self, 
        stream: BufferedIOBase, 
        filename: str | None = None,
        max_size: int | None = None,
        allowed_types: list[str] | None = None
    ) -> FileData:
        stream.seek(0, 2)
        size = stream.tell()

        if not size:
            raise EmptyFileError()

        if max_size and size > max_size:
            raise FileTooBigError(
                values = {
                    "size": size,
                    "filename": filename,
                    "max_file_size": max_size
                }
            )

        stream.seek(0)
        mime_type = self.MIME_VALIDATOR.from_buffer(stream.read())

        if allowed_types and not mime_type in allowed_types:
            raise UnsupportedFileFormatError(
                message="Unsuported file format",
                values = {
                    "format": mime_type,
                    "filename": filename,
                    "allowed_types": allowed_types
                }
            )
        
        # TODO: Adicionar yield aq pra processar em paralelo
        if mime_type.startswith('audio/'):
            await self.audio_validator(stream)

        elif mime_type.startswith('image/'):
            await asyncio.to_thread(self.image_validator, stream)

        else:
            raise UnsupportedFileFormatError(
                message="Unsuported file format",
                values = {
                    "format": mime_type,
                    "filename": filename
                }
            )

        return FileData(
            stream=stream,
            mime_type=mime_type,
            size=size
        )