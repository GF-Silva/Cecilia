from .schemas import ErrorDetails
from fastapi.responses import Response, JSONResponse
from typing import Any, Mapping
from pydantic import BaseModel

COMMON_ERRORS = {
    400: {
        "model": ErrorDetails,
        "description": "Invalid data"
    },
    404: {
        "model": ErrorDetails,
        "description": "Resource not found"
    }
}

class BaseResponse(BaseModel):
    title: str
    message: str
    values: dict[str, Any] | None = None
    status_code: int = 200