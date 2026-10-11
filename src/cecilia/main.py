from fastapi import FastAPI
from scalar_fastapi import add_scalar_reference
from .routes.api import api_router

app = FastAPI(title="Cecília API")
add_scalar_reference(app)
app.include_router(api_router, prefix='/api')