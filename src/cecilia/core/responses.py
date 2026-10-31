from .schemas import ErrorDetails

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