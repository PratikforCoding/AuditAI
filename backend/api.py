"""
Main FastAPI application setup
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

from backend.config.settings import settings
from backend.utils.logger import get_logger
from backend import api_auth, api_agents

# Initialize logger
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AuditAI Backend",
    description="Infrastructure audit and cost optimization platform with AI-powered recommendations",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ===== CORS Configuration =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        settings.FRONTEND_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Error Handlers =====

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# ===== Middleware =====

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# ===== Health Check Endpoints =====

@app.get("/api/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": "AuditAI Backend",
        "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/status")
async def system_status():
    """Detailed system status"""
    try:
        from backend.models.database import db
        
        mongodb_status = "healthy"
        try:
            db.ping()
        except:
            mongodb_status = "unhealthy"
        
        return {
            "status": "healthy",
            "components": {
                "mongodb": mongodb_status,
                "gemini_api": "healthy",
                "gcp": "configured"
            },
            "version": "2.0.0",
            "environment": settings.ENVIRONMENT,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Status check failed: {str(e)}")
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

# ===== Include Routers =====

app.include_router(api_auth.router)
app.include_router(api_agents.router)

# ===== Startup/Shutdown Events =====

@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("=" * 60)
    logger.info("🚀 AuditAI Backend Server Starting")
    logger.info("=" * 60)
    logger.info(f"📍 API Server: http://{settings.HOST}:{settings.PORT}")
    logger.info(f"📚 API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    logger.info(f"🔍 Alternative Docs: http://{settings.HOST}:{settings.PORT}/redoc")
    logger.info(f"🔐 Authentication: JWT Token Required")
    logger.info(f"📊 Database: MongoDB ({settings.DATABASE_NAME})")
    logger.info(f"🤖 AI Model: {settings.GEMINI_MODEL}")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("=" * 60)
    logger.info("⛔ AuditAI Backend Server Shutting Down")
    logger.info("=" * 60)

# ===== Root Endpoint =====

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "AuditAI Backend",
        "version": "2.0.0",
        "docs": "http://localhost:8000/docs",
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )