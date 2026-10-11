from groq import AsyncGroq
from cecilia.core.settings import settings

client = AsyncGroq(
    api_key = settings.groq.api_key
)