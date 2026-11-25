from typing import Any
from cecilia.core.exceptions import BaseError

class UnsupportedFileFormatError(BaseError):
    def __init__(
        self,
        format: str,
        title: str = "Unsupported file format",
        status_code: int = 415,
        error_code: str = "UNSUPORTED_FILE_FORMAT",
        values: dict[str, Any] | None = None
    ):
        self.status_code = status_code
        self.title = title
        self.format = format
        self.error_code = error_code
        self.values = values

        super().__init__(
            status_code=status_code,
            title=title,
            message=f'The format {format} is not supported',
            error_code=error_code,
            values=values
        )
