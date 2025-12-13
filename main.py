"""
AuditAI Backend - Main Entry Point
Starts the FastAPI server for infrastructure auditing and cost optimization
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import uvicorn

# Import router from api
from backend.api import router
from backend.config.settings import settings
from backend.config.database import DatabaseConnection

# Setup logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ===== LIFESPAN CONTEXT MANAGER =====

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage app startup and shutdown
    """
    # STARTUP
    try:
        logger.info("=" * 60)
        logger.info("🚀 Starting AuditAI Backend Server")
        logger.info("=" * 60)
        
        # Connect to database
        logger.info("📊 Connecting to MongoDB...")
        DatabaseConnection.connect()
        logger.info("✅ Database connected successfully")
        
        logger.info("📍 API Server: http://localhost:8000")
        logger.info("📚 API Documentation: http://localhost:8000/docs")
        logger.info("🔍 Alternative Docs: http://localhost:8000/redoc")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise
    
    yield  # Server runs here
    
    # SHUTDOWN
    try:
        logger.info("=" * 60)
        logger.info("🛑 Shutting down AuditAI Backend")
        logger.info("=" * 60)
        
        # Disconnect from database
        DatabaseConnection.disconnect()
        logger.info("✅ Database disconnected")
        
    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")


# ===== CREATE FASTAPI APP =====

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Infrastructure Auditing & Cost Optimization API",
    lifespan=lifespan
)


# ===== MIDDLEWARE =====

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== ROUTES =====

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "online"
    }

# Include router with all endpoints
app.include_router(router)


# ===== MAIN ENTRY POINT =====

def main():
    """Start the FastAPI server"""
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True,
    )


if __name__ == "__main__":
    main()