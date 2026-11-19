from .openrouter.completions import Completions
from .cloudflare.r2 import R2
from .cloudflare.clients import r2_manager
from fastapi import Depends
from typing import Annotated
from cecilia.core.settings import settings
from cecilia.core.exceptions import InternalError

def get_openrouter_completion_integration():
    return Completions(
        api_key=settings.openrouter.api_key,
        api_client=settings.api_client
    )

def get_r2_integration():
    if not r2_manager.client:
        raise InternalError()
    
    return R2(r2_manager.client)

OpenrouterCompletionIntegrationDep = Annotated[Completions, Depends(get_openrouter_completion_integration)]
R2IntegrationDep = Annotated[R2, Depends(get_r2_integration)]