from pydantic_settings import BaseSettings, SettingsConfigDict

class GroqSettings(BaseSettings):
    api_key: str
    stt_model: str = "whisper-large-v3"
    stt_language: str = "pt"
    llm_model: str = "openai/gpt-oss-120b"
    system_prompt: str = "Você é uma assistente feliz e alegre, sempre disponivel para ajudar"

class AzureSettings(BaseSettings):
    speech_key: str
    speech_region: str = "brazilsouth"
    speech_synthesis_voice_name: str = 'pt-BR-ThalitaNeural'

class OpenRouterSettings(BaseSettings):
    api_key: str
    server_url: str = "https://ai.hackclub.com/proxy/v1"
    system_prompt: str = "Seu nome é Cecilia"

class Settings(BaseSettings):
    groq: GroqSettings
    azure: AzureSettings
    open_router: OpenRouterSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore"
    )


settings = Settings() # pyright: ignore[reportCallIssue]