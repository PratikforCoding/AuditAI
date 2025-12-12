"""
Application settings and environment variables
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # ===== Application =====
    APP_NAME: str = "AuditAI"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = Field(default="development", description="Environment: development, staging, production")
    DEBUG: bool = Field(default=False, description="Debug mode")
    
    # ===== Server =====
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    
    # ===== GCP =====
    GOOGLE_PROJECT_ID: str = Field(default="", description="GCP Project ID")
    GOOGLE_API_KEY: str = Field(default="", description="Google API Key")
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = Field(default=None, description="Path to service account JSON")
    
    # ===== Gemini AI =====
    GEMINI_MODEL: str = Field(default="gemini-2.0-flash", description="Gemini model to use")
    GEMINI_TEMPERATURE: float = Field(default=0.7, description="Temperature for generation")
    
    # ===== Database (MongoDB) =====
    MONGODB_URL: str = Field(default="mongodb://localhost:27017", description="MongoDB connection string")
    DATABASE_NAME: str = Field(default="auditai", description="Database name")
    USERS_COLLECTION: str = Field(default="users", description="Users collection name")
    ANALYSES_COLLECTION: str = Field(default="user_analyses", description="Analyses collection name")
    REPORTS_COLLECTION: str = Field(default="audit_reports", description="Reports collection name")
    
    # ===== Authentication & Security =====
    SECRET_KEY: str = Field(default="", description="JWT secret key")
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_HOURS: int = Field(default=24, description="Token expiration hours")
    
    # ===== Encryption =====
    ENCRYPTION_KEY: str = Field(default="", description="Fernet encryption key for credentials")
    
    # ===== Frontend =====
    FRONTEND_URL: str = Field(default="http://localhost:3000", description="Frontend URL for CORS")
    
    # ===== Logging =====
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FILE: str = Field(default="logs/auditai.log", description="Log file path")
    ERROR_LOG_FILE: str = Field(default="logs/error.log", description="Error log file path")
    
    # ===== API Rate Limiting =====
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Enable rate limiting")
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Requests per minute")
    
    class Config:
        env_file = ".env.local"
        case_sensitive = True
        extra = "ignore"


# Create settings instance
settings = Settings()

# Validate critical settings in production
if settings.ENVIRONMENT == "production":
    assert settings.SECRET_KEY, "SECRET_KEY must be set in production"
    assert settings.ENCRYPTION_KEY, "ENCRYPTION_KEY must be set in production"
    assert settings.GOOGLE_PROJECT_ID, "GOOGLE_PROJECT_ID must be set in production"
    assert settings.GOOGLE_API_KEY, "GOOGLE_API_KEY must be set in production"