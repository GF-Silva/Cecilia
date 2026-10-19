from fastapi import FastAPI
from scalar_fastapi import add_scalar_reference
from .routes.api import api_router

from cecilia.core.database import create_db_and_tables

app = FastAPI(title="Cecília API")

add_scalar_reference(app)
app.include_router(api_router, prefix='/api')

@app.on_event("startup")
def on_startup():
    create_db_and_tables()