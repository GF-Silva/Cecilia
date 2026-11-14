from cecilia.core.exceptions import BaseError
from typing import Any

# TODO: Move all validation related class to here
class FileError(BaseError):
    def __init__(
        self,
        title: str = 'File error',
        status_code: int = 422,
        message: str = 'The file is invalid',
        error_code: str = 'FILE_ERROR',
        values: dict[str, Any] | None = None
    ):
        super().__init__(title=title, status_code=status_code, message=message, error_code=error_code, values=values)

class EmptyFileError(FileError):
    def __init__(
        self,
        title: str = 'File empty',
        status_code: int = 422,
        message: str = 'The file content should not be empty',
        error_code: str = 'FILE_EMPTY'
    ):
        super().__init__(title=title, status_code=status_code, message=message, error_code=error_code)

class InvalidFileType(FileError):
    def __init__(
        self,
        title: str = 'Invalid file type',
        status_code: int = 422,
        message: str = 'The file type is not valid',
        error_code: str = 'INVALID_FILE_TYPE',
        type: str | None = None
    ):
        super().__init__(title=title, status_code=status_code, message=message, error_code=error_code, values={
            "type": type
        })