from cecilia.adapters import FFProbeAdapter
from typing import BinaryIO
from cecilia.core.exceptions import InvalidFileError
from .errors import EmptyFileError, InvalidFileType
import magic

# TODO: Add more audio validations
class AudioValidator:
    MIME_VALIDATOR = magic.Magic(mime=True)

    def __init__(
        self,
        ffprobe_adapter: FFProbeAdapter
    ) -> None:
        self.ffprobe_adapter = ffprobe_adapter

    async def __call__(self, stream: BinaryIO):
        stream.seek(0)
        data = stream.read()

        if not data:
            raise EmptyFileError()
        
        mime_type = self.MIME_VALIDATOR.from_buffer(data)

        if not mime_type.startswith('audio/'):
            raise InvalidFileType(message='The file is not an audio')

        file_metadata = await self.ffprobe_adapter.validate_file_from_buffer(data)

        if not file_metadata.format.duration or not file_metadata.format.duration > 0:
            raise InvalidFileError()
        