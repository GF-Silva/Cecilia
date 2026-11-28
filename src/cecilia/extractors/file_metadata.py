from dataclasses import dataclass
from io import BufferedIOBase
import magic

@dataclass
class FileMetadata:
    mime_type: str
    size: int

class FileMetadataExtractor:
    _MAGIC_EXTRACTOR = magic.Magic(mime=True)

    def __call__(self, file: BufferedIOBase) -> FileMetadata:
        mime_type = self._MAGIC_EXTRACTOR.from_buffer(file.read(248_000))
        file.seek(0, 2)
        size = file.tell()

        return FileMetadata(
            mime_type=mime_type,
            size=size
        )