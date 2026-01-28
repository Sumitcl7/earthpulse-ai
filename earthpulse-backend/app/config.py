from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # ======================
    # App Settings
    # ======================
    APP_NAME: str = "EarthPulse AI"
    DEBUG: bool = True

    # ======================
    # Database
    # ======================
    DATABASE_URL: str = "postgresql://user:password@localhost/earthpulse"

    # ======================
    # API Keys (Optional)
    # ======================
    SENTINEL_HUB_CLIENT_ID: Optional[str] = None
    SENTINEL_HUB_CLIENT_SECRET: Optional[str] = None
    NEWS_API_KEY: Optional[str] = None

    # ======================
    # Google Earth Engine (Optional)
    # ======================
    GOOGLE_EARTH_ENGINE_KEY: Optional[str] = None
    EE_SERVICE_ACCOUNT: Optional[str] = None
    EE_KEY_FILE: Optional[str] = None

    # ======================
    # Pydantic Config (v2)
    # ======================
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"   # 🚀 Ignore unknown .env vars instead of crashing


@lru_cache()
def get_settings():
    return Settings()
