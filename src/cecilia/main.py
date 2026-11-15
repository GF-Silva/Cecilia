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
from starlette.routing import WebSocketRoute
import uuid
import os
import arel

DEBUG = os.getenv('DEBUG', "0") == "1"
templates = Jinja2Templates(directory='src/cecilia/routes/web')
templates.env.globals['DEBUG'] = DEBUG

hot_reload = None
if DEBUG:
    hot_reload = arel.HotReload(paths=[arel.Path('src/cecilia/routes/web')])
    templates.env.globals['hot_reload'] = hot_reload

@asynccontextmanager
async def lyfespan(app: FastAPI):
    database.create_db_and_tables()

    await r2_manager.startup()
    if hot_reload:
        await hot_reload.startup()

    yield

    await r2_manager.shutdown()

    if hot_reload:
        await hot_reload.shutdown()

app = FastAPI(title="Cecília API", lifespan=lyfespan)

if hot_reload:
    app.router.routes.append(WebSocketRoute(
        '/hot-reload', hot_reload, name='hot-reload'
    ))

app.mount('/static', StaticFiles(directory='src/cecilia/routes/web'), name='static')

@app.get('/', response_class = HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, 'index.html')

@app.get('/chats/{chat_id}', response_class=HTMLResponse)
async def chat(request: Request, chat_id: uuid.UUID):
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

