# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Import ALL routers
from api import router as api_router
from api_auth import router as auth_router
from api_onboarding import router as onboarding_router
from api_agents import router as agent_router
from config.settings import settings
from config.database import DatabaseConnection
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # STARTUP
    logger.info("🚀 Starting AuditAI Backend")
    DatabaseConnection.connect()
    logger.info("✅ Database connected")
    
    yield  # Server runs here
    
    # SHUTDOWN
    logger.info("🛑 Shutting down")
    DatabaseConnection.disconnect()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Infrastructure Auditing & Cost Optimization API",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "online"
    }

# Include ALL routers
app.include_router(api_router)           # Basic endpoints
app.include_router(auth_router)          # Auth endpoints
app.include_router(onboarding_router)    # Onboarding endpoints
app.include_router(agent_router)         # AI Agent endpoints


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )