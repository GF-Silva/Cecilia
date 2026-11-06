import asyncio
import json
from .types import FFProbeResponse

class FFProbeAdapter:
    async def validate_file_from_buffer(self, file_data: bytes):
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

        stdout, stderr = await process.communicate(input=file_data)

        if process.returncode != 0:
            error_msg = stderr.decode('utf-8').strip()
            print(error_msg)
            return

        try:
            data: FFProbeResponse = FFProbeResponse.model_validate(json.loads(stdout.decode('utf-8')))

            streams = data.streams
            audio_streams = [
                stream for stream in streams if stream.codec_type == 'audio'
            ]

            if not audio_streams:
                print("not a single audio stream")
                return

            format = data.format

            print(format)
            print(format.format_name)
            print(format.tags)

        except json.JSONDecodeError as err:
            print(str(err))