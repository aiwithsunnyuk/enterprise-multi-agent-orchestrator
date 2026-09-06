from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str = "mock-key"
    orchestrator_model: str = "mock-model"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
