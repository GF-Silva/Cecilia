from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from scalar_fastapi import add_scalar_reference
from fastapi.responses import JSONResponse
from httpx import TimeoutException

from .routes import api_router
from cecilia.core import database, exceptions, schemas
from cecilia.integrations.cloudflare.clients import r2_manager

# TODO: Temporary only, remove after creating frontend
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

@asynccontextmanager
async def lyfespan(app: FastAPI):
    database.create_db_and_tables()

    await r2_manager.startup()

    yield

    await r2_manager.shutdown()

app = FastAPI(title="Cecília API", lifespan=lyfespan)

app.mount('/static', StaticFiles(directory='src/cecilia/routes/web'), name='static')

templates = Jinja2Templates(directory='src/cecilia/routes/web')

@app.get('/', response_class = HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, 'index.html')

add_scalar_reference(app)
app.include_router(api_router)

@app.exception_handler(exceptions.BaseError)
def error_handler(_, exception: exceptions.BaseError):
    error = schemas.ErrorDetails(
        title=exception.title,
        status_code=exception.status_code,
        detail=exception.message,
        type=exception.error_code,
        extra_info=exception.values
    )

    return JSONResponse(
        status_code=error.status_code,
        content=error.model_dump(exclude_unset=True)
    )

@app.exception_handler(Exception)
def internal_error_handler(_, exception: Exception):
    error = schemas.ErrorDetails(
        title='Internal server Error',
        status_code=500,
        detail='Something unexpected happened, maybe try again after a while?',
        type='INTERNAL_ERROR'
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

