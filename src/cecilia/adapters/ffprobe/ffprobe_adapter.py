import asyncio
import json
from .types import FFProbeResponse
from cecilia.core.exceptions import InvalidFileError, InternalError

class FFProbeAdapter:
    async def validate_file_from_buffer(self, file_data: bytes) -> FFProbeResponse:
        command = [
            'ffprobe',
            '-v', 'error',
            '-show_format',
            '-show_streams',
            '-of', 'json',
            'pipe:0'
        ]

        process = await asyncio.create_subprocess_exec(
            *command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, _ = await process.communicate(input=file_data)

        if process.returncode != 0:
            raise InternalError()

        try:
            data = FFProbeResponse.model_validate(json.loads(stdout.decode('utf-8')))

            streams = data.streams
            audio_streams = [
                stream for stream in streams if stream.codec_type == 'audio'
            ]

            if not audio_streams:
                raise InvalidFileError()
            
            return data

        except json.JSONDecodeError as err:
            raise InternalError()