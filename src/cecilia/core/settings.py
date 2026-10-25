from pydantic_settings import BaseSettings, SettingsConfigDict

class OpenRouterSettings(BaseSettings):
    api_key: str
    server_url: str = "https://ai.hackclub.com/proxy/v1"
    system_prompt: str = "Seu nome é Cecilia"

class Settings(BaseSettings):
    open_router: OpenRouterSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore"
    )


settings = Settings() # pyright: ignore[reportCallIssue]