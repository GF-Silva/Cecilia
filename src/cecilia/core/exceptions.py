from typing import Any

class BaseError(Exception):
    def __init__(
        self, 
        title: str,
        status_code: int,
        message: str, 
        error_code: str, 
        values: dict[str, Any] | None = None

    ) -> None:
        self.title = title
        self.status_code = status_code
        self.message=message
        self.error_code=error_code
        self.values=values

        super().__init__({
            "message": message,
            "error_code": error_code,
            "values": values,
            "title": title,
            "status_code": status_code
        })

class InternalError(BaseError):
    def __init__(
        self, 
        message: str = "something unexpected happened, maybe try again after a while?", 
        error_code: str = "INTERNAL_ERROR",
        title: str = "Internal Server Error",
        status_code: int = 500,
        values: dict[str, Any] | None = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.title = title

        super().__init__(
            message=message,
            error_code=error_code,
            values=values,
            title=title,
            status_code=status_code
        )

class NotFoundError(BaseError):
    def __init__(
        self, 
        resource: str, 
        item: Any, 
        status_code: int = 404,
        title: str = "Resource not found",
        error_code: str = "NOT_FOUND", 
        values: dict | None = None
    ):
        self.title = title
        self.resource = resource
        self.status_code = status_code
        self.item = item
        self.error_code = error_code
        self.values = values

        super().__init__(
            title=title,
            status_code=status_code,
            message=f"{resource} does not have the item identified by {item}",
            error_code=error_code,
            values=values
        )

class ValueError(BaseError):
    def __init__(
        self,
        message: str,
        title: str = "Value Error",
        status_code: int = 400,
        error_code: str = "VALUE_ERROR",
        values: dict[str, Any] | None = None
    ):
        self.message = message
        self.error_code=error_code
        self.values=values
        
        super().__init__(
            title=title,
            status_code=status_code,
            message=message,
            error_code=error_code,
            values=values
        )

class UnsupportedFileFormatError(BaseError):
    def __init__(
        self,
        message: str,
        title: str = "Unsupported file format",
        status_code: int = 415,
        error_code: str = "UNSUPORTED_FILE_FORMAT",
        values: dict[str, Any] | None = None
    ):
        self.status_code = status_code
        self.title = title
        self.message = message
        self.error_code = error_code
        self.values = values

        super().__init__(
            status_code=status_code,
            title=title,
            message=message,
            error_code=error_code,
            values=values
        )

# TODO: Mostrar o nome do arquivo
class InvalidFileError(BaseError):
    def __init__(
        self,
        title: str = "Invalid file content",
        status_code: int = 422,
        message: str = "The file content is invalid",
        error_code: str = "INVALID_FILE",
        values: dict[str, Any] | None = None
    ):
        self.title = title
        self.status_code = status_code
        self.message = message
        self.error_code = error_code
        self.values = values

        super().__init__(
            title=title,
            message=message,
            status_code=status_code,
            error_code=error_code,
            values=values
        )

class FileTooBigError(BaseError):
    def __init__(
        self,
        title: str = "File too big",
        status_code: int = 413,
        message: str = "The given file is big to process",
        error_code: str = "FILE_TOO_BIG",
        values: dict[str, Any] | None = None
    ):
        self.status_code = status_code
        self.title = title
        self.message = message
        self.error_code = error_code
        self.values = values

        super().__init__(
            status_code=status_code,
            title=title,
            message=message,
            error_code=error_code,
            values=values
        )