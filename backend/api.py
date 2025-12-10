"""
AuditAI Backend API
Infrastructure auditor powered by Gemini AI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from backend import api_agents  # ← ADD THIS LINE

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AuditAI API",
    description="Infrastructure auditor for GCP using Gemini AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include AI Agent router ← ADD THIS BLOCK
app.include_router(api_agents.router)

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AuditAI Backend",
        "version": "1.0.0"
    }

@app.get("/api/status")
async def status():
    """Get service status"""
    return {
        "gcp_connected": True,
        "mongodb_connected": False,
        "gemini_ready": True,
        "available_endpoints": [
            "/api/v1/agent/analyze",
            "/api/v1/agent/suggestions",
            "/api/v1/agent/execute-plan",
            "/api/v1/agent/report",
            "/api/v1/agent/health"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
