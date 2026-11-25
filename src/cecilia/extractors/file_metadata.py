from dataclasses import dataclass
from typing import BinaryIO
import magic

@dataclass
class FileMetadata:
    mime_type: str

class FileMetadataExtractor:
    _MAGIC_EXTRACTOR = magic.Magic(mime=True)

    def __call__(self, file: BinaryIO) -> FileMetadata:
        mime_type = self._MAGIC_EXTRACTOR.from_buffer(file.read(248_000))

        return FileMetadata(
            mime_type=mime_type
        )