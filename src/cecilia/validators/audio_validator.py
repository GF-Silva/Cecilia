from cecilia.adapters import FFProbeAdapter
from typing import BinaryIO
from cecilia.core.exceptions import InvalidFileError
from .errors import EmptyFileError, InvalidFileType
from .responses import FileData
import magic

# TODO: Add more audio validations
class AudioValidator:
    def __init__(
        self,
        ffprobe_adapter: FFProbeAdapter
    ):
        self.ffprobe_adapter = ffprobe_adapter

    async def __call__(self, stream: BinaryIO):
        stream.seek(0)
        data = stream.read()

        if not data:
            raise EmptyFileError()

        await self.ffprobe_adapter.validate_file_from_buffer(data)