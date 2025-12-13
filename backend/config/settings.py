"""
Application settings and configuration
Updated with MongoDB Atlas configuration
FIXED for Pydantic v2
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # ===== Pydantic v2 Configuration =====
    model_config = ConfigDict(
        extra='ignore',              # ✅ Ignores frontend vars (NEXT_PUBLIC_*, etc)
        env_file='.env.local',       # ✅ Loads .env.local automatically
        env_ignore_empty=True,       # ✅ Ignores empty environment variables
        case_sensitive=False         # ✅ Flexible with env var names
    )
    
    # ===== Environment =====
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # ===== Application =====
    APP_NAME: str = "AuditAI"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # ===== Server =====
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:3000"
    
    # ===== Security =====
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    ENCRYPTION_KEY: str
    
    # ===== MongoDB Atlas Configuration =====
    MONGODB_URL: str
    DATABASE_NAME: str = "auditai"
    
    # MongoDB Collection Names
    USERS_COLLECTION: str = "users"
    ANALYSES_COLLECTION: str = "user_analyses"
    REPORTS_COLLECTION: str = "audit_reports"
    COST_ANALYSES_COLLECTION: str = "cost_analyses"
    SUBSCRIPTIONS_COLLECTION: str = "subscriptions"
    
    # ===== GCP Configuration =====
    GOOGLE_PROJECT_ID: str = ""
    GOOGLE_API_KEY: str = ""
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None
    
    # ===== Gemini AI Configuration =====
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_TEMPERATURE: float = 0.7
    
    # ===== Feature Flags =====
    ENABLE_ANALYSIS_CACHING: bool = True
    ANALYSIS_CACHE_TTL: int = 3600  # 1 hour
    
    # ===== Rate Limiting =====
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # ===== Logging =====
    LOG_FILE: str = "logs/app.log"
    
    # ===== Helper Methods =====
    
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT.lower() == "production"
    
    def get_mongodb_connection_string(self) -> str:
        """Get MongoDB connection string"""
        return self.MONGODB_URL
    
    def validate_mongodb_config(self) -> bool:
        """Validate MongoDB configuration"""
        if not self.MONGODB_URL:
            raise ValueError("MONGODB_URL not configured in .env.local")
        if not self.DATABASE_NAME:
            raise ValueError("DATABASE_NAME not configured in .env.local")
        return True
    
    def validate_secrets(self) -> bool:
        """Validate critical secrets"""
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY not configured in .env.local")
        if not self.ENCRYPTION_KEY:
            raise ValueError("ENCRYPTION_KEY not configured in .env.local")
        return True


# Global settings instance
settings = Settings()