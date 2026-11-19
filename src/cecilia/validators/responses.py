from dataclasses import dataclass
from typing import BinaryIO

@dataclass
class FileData:
    stream: BinaryIO
    mime_type: str | None = None
    size: int | None = None