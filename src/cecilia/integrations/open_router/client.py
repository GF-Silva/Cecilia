from openrouter import OpenRouter
from cecilia.core.settings import settings

client = OpenRouter(
    api_key=settings.open_router.api_key,
    server_url=settings.open_router.server_url
)

guest_client = OpenRouter()