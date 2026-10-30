from fastapi import FastAPI, Request
from scalar_fastapi import add_scalar_reference
from fastapi.responses import JSONResponse
from httpx import TimeoutException

from .routes import api_router
from cecilia.core import database, exceptions, schemas

app = FastAPI(title="Cecília API")

add_scalar_reference(app)
app.include_router(api_router)

@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()

@app.exception_handler(exceptions.ValueError)
def value_error_handler(_, exception: exceptions.NotFoundError):
    error = schemas.ErrorDetails(
        title="Value Error",
        status_code=400,
        detail=exception.message,
        type=exception.error_code,
        extra_info=exception.values
    )

    return JSONResponse(
        status_code=error.status_code,
        content=error.model_dump(exclude_unset=True)
    )

@app.exception_handler(exceptions.NotFoundError)
def not_found_error_handler(request: Request, exception: exceptions.NotFoundError):
    error = schemas.ErrorDetails(
        title="Resource not found",
        status_code=404,
        detail=exception.message,
        type=exception.error_code,
        extra_info=exception.values
    )

    return JSONResponse(
        status_code=error.status_code,
        content=error.model_dump(exclude_unset=True)
    )

@app.exception_handler(exceptions.InternalError)
def internal_error_handler(request: Request, exception: exceptions.InternalError):
    error = schemas.ErrorDetails(
        title="Internal server error",
        status_code=500,
        detail=exception.message,
        type=exception.error_code,
        extra_info=exception.values
    )

    return JSONResponse(
        status_code=error.status_code,
        content=error.model_dump(exclude_unset=True)
    )

@app.exception_handler(TimeoutException)
async def read_timeout_handler(request: Request, exception: TimeoutException):
    return JSONResponse(
        status_code=504,
        content={
            "detail": "timed out while receiving data"
        }
    )