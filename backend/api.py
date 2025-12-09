"""
AuditAI Backend API
Infrastructure auditor powered by Gemini AI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AuditAI API",
    description="Infrastructure auditor for GCP using Gemini AI",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AuditAI Backend",
        "version": "0.1.0"
    }

@app.get("/api/status")
async def status():
    """Get service status"""
    return {
        "gcp_connected": False,
        "mongodb_connected": False,
        "gemini_ready": False
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
