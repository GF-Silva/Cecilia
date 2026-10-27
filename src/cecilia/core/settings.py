from pydantic_settings import BaseSettings, SettingsConfigDict
import httpx
class OpenRouterSettings(BaseSettings):
    api_key: str
    server_url: str = "https://ai.hackclub.com/proxy/v1"
    system_prompt: str = "Seu nome é Cecilia"

class HackclubAISettings(BaseSettings):
    api_key: str
    server_url: str = "https://ai.hackclub.com/proxy/v1"
    completions_url: str = f"{server_url}/chat/completions"

class Settings(BaseSettings):
    open_router: OpenRouterSettings
    hackclub_ai: HackclubAISettings
    api_client: httpx.AsyncClient = httpx.AsyncClient()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore"
    )


settings = Settings() # pyright: ignore[reportCallIssue]