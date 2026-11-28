from dataclasses import dataclass
from io import BufferedIOBase

@dataclass
class FileData:
    stream: BufferedIOBase
    mime_type: str | None = None
    size: int | None = None