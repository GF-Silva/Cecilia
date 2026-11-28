from cecilia.adapters import FFProbeAdapter
from io import BufferedIOBase
from .errors import EmptyFileError

# TODO: Add more audio validations
class AudioValidator:
    def __init__(self, ffprobe_adapter: FFProbeAdapter):
        self.ffprobe_adapter = ffprobe_adapter

    async def __call__(self, stream: BufferedIOBase):
        stream.seek(0)
        data = stream.read()

        if not data:
            raise EmptyFileError()

        return await self.ffprobe_adapter.validate_file_from_buffer(data)