from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = 'development'
    SECRET_KEY: str = 'change_me_in_production'
    REDIS_URL: str = 'redis://localhost:6379'
    WS_PING_INTERVAL: int = 20
    WS_PING_TIMEOUT: int = 10
    OBD_POLL_INTERVAL_MS: int = 500
    CORS_ORIGINS: list[str] = ['*']
    EXPECTED_API_KEY: str = 'automat_secret_key'

    class Config:
        env_file = '.env'

@lru_cache
def get_settings() -> Settings:
    return Settings()