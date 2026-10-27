from fastapi import FastAPI, Request
from scalar_fastapi import add_scalar_reference
from fastapi.responses import JSONResponse
from .routes import api_router

from cecilia.core.database import create_db_and_tables

app = FastAPI(title="Cecília API")

add_scalar_reference(app)
app.include_router(api_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exception: ValueError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exception)
        }
    )

@app.exception_handler(LookupError)
async def lookup_error_handler(request: Request, exception: LookupError):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exception)
        }
    )