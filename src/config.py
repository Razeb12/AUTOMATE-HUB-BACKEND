from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str
    SECRET_KEY: str
    REDIS_URL: str
    WS_PING_INTERVAL: int
    WS_PING_TIMEOUT: int
    OBD_POLL_INTERVAL_MS: int
    CORS_ORIGINS: list[str]
    EXPECTED_API_KEY: str

    class Config:
        env_file = '.env'

@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore