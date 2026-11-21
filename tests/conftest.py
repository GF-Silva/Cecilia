import pytest
from dataclasses import dataclass
from typing import BinaryIO

@dataclass
class FileData:
    stream: BinaryIO
    mime_type: str
    size: int
    filename: str
    type: str
    public_filename: str

@pytest.fixture
def file():
    def _factory(
        mime_type: str = 'audio/mpeg',
        type: str = 'mp3',
        filename: str = 'audio',
        public_filename: str = 'audio of something'
    ):
        file = open(f'tests/fixtures/{mime_type}/{filename}.{type}', 'rb')
        file.seek(0, 2)
        size = file.tell()
        file.seek(0)

        yield FileData(
            mime_type=mime_type,
            size=size,
            stream=file,
            filename=filename,
            type=type,
            public_filename=public_filename
        )

        file.close()
        
    return _factory