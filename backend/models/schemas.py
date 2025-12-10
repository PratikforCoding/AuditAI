"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ResourceType(str, Enum):
    COMPUTE = "compute"
    STORAGE = "storage"
    DATABASE = "database"
    NETWORKING = "networking"
    BIGQUERY = "bigquery"
    CONTAINER = "container"
    OTHER = "other"

class ResourceStatus(str, Enum):
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    IDLE = "IDLE"
    ERROR = "ERROR"
    PENDING = "PENDING"
    UNKNOWN = "UNKNOWN"

class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

# Request/Response Schemas
class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., example="healthy")
    service: str = Field(..., example="AuditAI back-end")
    version: str = Field(..., example="0.1.0")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusResponse(BaseModel):
    """System status response"""
    gcp_connected: bool = Field(..., example=False)
    mongodb_connected: bool = Field(..., example=False)
    gemini_ready: bool = Field(..., example=False)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Resource(BaseModel):
    """GCP Resource"""
    id: str = Field(..., description="Resource ID")
    name: str = Field(..., description="Resource name")
    type: ResourceType = Field(..., description="Resource type")
    status: ResourceStatus = Field(..., description="Resource status")
    zone: Optional[str] = Field(None, description="Resource zone")
    cpu_cores: Optional[int] = Field(None, description="Number of CPU cores")
    cpu_usage: Optional[float] = Field(None, ge=0, le=100, description="CPU usage percentage")
    memory_gb: Optional[float] = Field(None, description="Memory in GB")
    memory_usage: Optional[float] = Field(None, ge=0, le=100, description="Memory usage percentage")
    disk_gb: Optional[float] = Field(None, description="Disk in GB")
    disk_usage: Optional[float] = Field(None, ge=0, le=100, description="Disk usage percentage")
    monthly_cost: Optional[float] = Field(None, ge=0, description="Monthly cost in USD")
    created: Optional[datetime] = Field(None, description="Creation timestamp")
    last_modified: Optional[datetime] = Field(None, description="Last modification timestamp")
    tags: Optional[List[str]] = Field(None, description="Resource tags")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "prod-1",
                "name": "Production Server",
                "type": "compute",
                "status": "RUNNING",
                "zone": "us-central1-a",
                "cpu_cores": 4,
                "cpu_usage": 15.5,
                "memory_gb": 16,
                "memory_usage": 42.3,
                "disk_gb": 100,
                "disk_usage": 73.1,
                "monthly_cost": 125.50,
            }
        }


class Recommendation(BaseModel):
    """Audit recommendation"""
    id: str = Field(..., description="Recommendation ID")
    resource_id: str = Field(..., description="Related resource ID")
    title: str = Field(..., description="Recommendation title")
    description: Optional[str] = Field(None, description="Detailed description")
    severity: Severity = Field(..., description="Severity level")
    monthly_savings: Optional[float] = Field(None, ge=0, description="Monthly savings in USD")
    risk_level: Severity = Field(..., description="Implementation risk level")
    difficulty: str = Field(..., description="Implementation difficulty: Easy, Medium, Hard")
    ai_analysis: Optional[str] = Field(None, description="Gemini AI analysis")
    action_items: Optional[List[str]] = Field(None, description="Steps to implement")
    created: datetime = Field(default_factory=datetime.utcnow)
    dismissed: bool = Field(False, description="Is recommendation dismissed?")
    recommendation_type: str = "cost_optimization"
    annual_savings: float = 0.0
    confidence: float = 0.7
    source: str = "gcp_recommender_api"
    recommender_id: str = ""
    data_source: str = "production_api"

class AuditResult(BaseModel):
    """Audit result"""
    id: str = Field(..., description="Audit ID")
    timestamp: datetime = Field(..., description="Audit timestamp")
    resources_scanned: int = Field(..., ge=0, description="Number of resources scanned")
    issues_found: int = Field(..., ge=0, description="Number of issues found")
    total_savings: float = Field(..., ge=0, description="Total potential savings in USD")
    confidence_score: float = Field(..., ge=0, le=100, description="Confidence percentage")
    duration_seconds: Optional[float] = Field(None, ge=0, description="Audit duration")
    recommendations: List[Recommendation] = Field(default_factory=list)
    errors: Optional[List[str]] = Field(None, description="Any errors during audit")
    status: str = Field("completed", description="Audit status: completed, in_progress, failed")

class UserProfile(BaseModel):
    """User profile"""
    id: str = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email")
    name: Optional[str] = Field(None, description="User name")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    gcp_project_id: Optional[str] = Field(None, description="GCP project ID")
    created: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = Field(None)

class ApiResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool = Field(..., description="Operation success")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if failed")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {"key": "value"},
                "error": None,
                "timestamp": "2025-12-09T13:11:00Z"
            }
        }


# Usage:
# from models.schemas import Resource, Recommendation, ApiResponse
# resource = Resource(**data)
# response = ApiResponse(success=True, data=resource.dict())
