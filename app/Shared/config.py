from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str

    API_URL: str

    REQUEST_TIMEOUT: int = 30

    APP_ENV: str = "local"

    APP_DEBUG: bool = True

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()