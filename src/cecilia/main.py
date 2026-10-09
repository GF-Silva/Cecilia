from fastapi import FastAPI
from .routes.api import api_router

app = FastAPI(title="Cecília API")
app.include_router(api_router, prefix='/api')