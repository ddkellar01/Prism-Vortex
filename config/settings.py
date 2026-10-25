import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "PrismVortex"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    
    # API & Model Credentials
    GEMINI_API_KEY: str = ""
    ARGON_MODEL_ID: str = "gemini-4-argon"
    
    # External Data Services
    EARTH_ENGINE_PROJECT: str = "prism-vortex-geospatial"
    PEOPLE_SEARCH_API_URL: str = "https://api.peoplesearch.internal/v1/query"
    PEOPLE_SEARCH_API_KEY: str = ""
    FLOW_TELEMETRY_ENDPOINT: str = "https://flow.googleapis.com/v1/telemetry"
    
    # Infrastructure
    REDIS_URL: str = "redis://localhost:6379/0"
    HOST: str = "0.0.0.0"  # nosec B104
    PORT: int = 8080

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
