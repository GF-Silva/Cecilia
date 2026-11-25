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
        mime_type: str,                                 # Mime type of the file     - also the directory searched
        type: str,                                      # Type of the file          - Also the file extension
        filename: str = 'file1',                         # Name of the searched file - the name of the searched file
        public_filename: str = 'audio of something'     # Public name of the file   - just to display
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