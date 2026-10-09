# Junta as versoes v1 e etc
from fastapi import APIRouter
from .v1 import router_v1

api_router = APIRouter()

api_router.include_router(router_v1, prefix='/v1')