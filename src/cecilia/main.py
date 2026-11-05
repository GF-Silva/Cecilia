from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from scalar_fastapi import add_scalar_reference
from fastapi.responses import JSONResponse
from httpx import TimeoutException

from .routes import api_router
from cecilia.core import database, exceptions, schemas, settings
from cecilia.integrations.cloudflare.clients import r2_manager

@asynccontextmanager
async def lyfespan(app: FastAPI):
    database.create_db_and_tables()

    await r2_manager.startup(
        account_id = settings.settings.r2.account_id,
        access_key = settings.settings.r2.access_key,
        secret_key = settings.settings.r2.secret_access_key,
        region_name = settings.settings.r2.region
    )

    yield

    await r2_manager.shutdown()

app = FastAPI(title="Cecília API", lifespan=lyfespan)

add_scalar_reference(app)
app.include_router(api_router)

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

@app.exception_handler(exceptions.UnsupportedFileFormatError)
def unsupported_file_format_error_handler(request: Request, exception: exceptions.UnsupportedFileFormatError):
    error = schemas.ErrorDetails(
        title="Unsupported file format",
        status_code=415,
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