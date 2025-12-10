# AuditAI/main.py
"""
AuditAI Backend - Main Entry Point
Starts the FastAPI server for infrastructure auditing and cost optimization
"""

import uvicorn
import logging
from backend.api import app
from backend.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Start the FastAPI server"""
    logger.info("=" * 60)
    logger.info("🚀 Starting AuditAI Backend Server")
    logger.info("=" * 60)
    logger.info("📍 API Server: http://localhost:8000")
    logger.info("📚 API Documentation: http://localhost:8000/docs")
    logger.info("🔍 Alternative Docs: http://localhost:8000/redoc")
    logger.info("=" * 60)
    
    uvicorn.run(
        "backend.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True,
    )


if __name__ == "__main__":
    main()