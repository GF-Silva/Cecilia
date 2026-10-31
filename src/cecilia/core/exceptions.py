from typing import Any

class BaseError(Exception):
    def __init__(self, message: str, error_code: str, values: dict[str, Any] | None = None) -> None:
        self.message=message
        self.error_code=error_code
        self.values=values

        super().__init__({
            "message": message,
            "error_code": error_code,
            "values": values
        })

class InternalError(BaseError):
    def __init__(
        self, 
        message: str = "internal server error", 
        error_code: str = "INTERNAL_ERROR",
        values: dict | None = None
    ):
        self.message = message
        self.error_code = error_code

        super().__init__(
            message=message,
            error_code=error_code,
            values=values
        )

class NotFoundError(BaseError):
    def __init__(self, resource: str, item: Any, error_code: str = "NOT_FOUND", values: dict | None = None):
        self.resource = resource
        self.item = item
        self.error_code = error_code
        self.values = values

        super().__init__(
            message=f"{resource} does not have the item identified by {item}",
            error_code=error_code,
            values=values
        )

class ValueError(BaseError):
    def __init__(
        self,
        message: str,
        error_code: str = "VALUE_ERROR",
        values: dict[str, Any] | None = None
    ):
        self.message = message
        self.error_code=error_code
        self.values=values
        
        super().__init__(
            message=message,
            error_code=error_code,
            values=values
        )