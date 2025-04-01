from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/ad_optimization_db"
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Ad Optimization Platform"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Data ingestion settings
    BATCH_SIZE: int = 1000
    DATA_STORAGE_PATH: str = "./data"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create settings instance
config = Settings()