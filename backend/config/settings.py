"""
Configuration settings for AuditAI backend
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os
from functools import lru_cache
from datetime import datetime

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "AuditAI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Server
    API_HOST: str = "0.0.0.0"
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    API_PREFIX: str = "/api"
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://*.vercel.app",
    ]
    
    # Google Cloud
    GOOGLE_PROJECT_ID: str = os.getenv("GOOGLE_PROJECT_ID", "")
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", 
        "/Users/pratikkotal/Documents/Agent-Hack/auditai-sa.json"
    )
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # MongoDB
    MONGODB_URI: str = os.getenv(
        "MONGODB_URI", 
        ""
    )
    MONGODB_DB_NAME: str = "auditai"
    
    # JWT/Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Features
    ENABLE_AUDIT_SCHEDULING: bool = True
    AUDIT_FREQUENCY_HOURS: int = 24
    ENABLE_AGENTIC_AI: bool = True
    BILLING_EXPORT_DATASET: str = os.getenv("BILLING_EXPORT_DATASET", "billing_export")
    
    # Limits
    MAX_RESOURCES_PER_SCAN: int = 1000
    MAX_AUDIT_HISTORY: int = 100
    API_RATE_LIMIT: int = 100  # requests per minute
    
    class Config:
        env_file = ".env.local"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Export for easy importing
settings = get_settings()
