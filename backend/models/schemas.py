"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# ===== Authentication Models =====

class UserCreateRequest(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    company_name: Optional[str] = None


class UserLoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class AddCredentialsRequest(BaseModel):
    """Add GCP credentials request"""
    project_id: str = Field(..., description="GCP Project ID")
    service_account_json: str = Field(..., description="Service account JSON content")
    api_key: Optional[str] = None


class UserResponse(BaseModel):
    """User public information"""
    user_id: str
    email: EmailStr
    company_name: Optional[str]
    subscription_tier: str
    has_gcp_credentials: bool
    created: datetime


# ===== Analysis Models =====

class AnalysisRequest(BaseModel):
    """Infrastructure analysis request"""
    query: str = Field(..., description="Analysis query")
    days: int = Field(default=30, ge=1, le=365, description="Days to analyze")


class Recommendation(BaseModel):
    """Optimization recommendation"""
    id: str
    title: str
    description: str
    category: str  # compute, storage, database, networking
    resource_type: str
    severity: str  # Critical, High, Medium, Low
    estimated_savings: Optional[float]
    implementation_time: str  # Quick, Medium, Long
    confidence: float  # 0.0 to 1.0


class AnalysisResult(BaseModel):
    """Infrastructure analysis result"""
    status: str
    query: str
    analysis: str
    recommendations: List[Recommendation] = []
    total_cost_potential_savings: Optional[float]
    project_id: str
    days_analyzed: int
    generated_at: datetime


class UserAnalysisDB(BaseModel):
    """User analysis stored in database"""
    analysis_id: str
    user_id: str
    project_id: str
    query: str
    result: Dict[str, Any]
    cost_savings: Optional[float]
    created: datetime


# ===== Audit Report Models =====

class AuditReportRequest(BaseModel):
    """Generate audit report request"""
    days: int = Field(default=30, ge=1, le=365)
    include_recommendations: bool = True
    include_cost_analysis: bool = True


class AuditReport(BaseModel):
    """Comprehensive audit report"""
    report_id: str
    project_id: str
    user_id: str
    title: str
    executive_summary: str
    current_state: str
    findings: List[str]
    recommendations: List[str]
    cost_analysis: Dict[str, Any]
    priority_actions: List[str]
    estimated_roi: Optional[float]
    timeframe: str  # Quick wins, Medium-term, Strategic
    generated_at: datetime


# ===== Cost Analysis Models =====

class CostBreakdown(BaseModel):
    """Cost breakdown by service"""
    service: str
    current_cost: float
    projected_cost: Optional[float]
    potential_savings: Optional[float]
    percentage: float


class CostAnalysis(BaseModel):
    """Complete cost analysis"""
    project_id: str
    total_current_cost: float
    total_projected_cost: Optional[float]
    total_potential_savings: Optional[float]
    breakdown: List[CostBreakdown]
    trend: str  # Increasing, Stable, Decreasing
    analysis_date: datetime


# ===== API Response Models =====

class SuccessResponse(BaseModel):
    """Standard success response"""
    status: str = "success"
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str
    status_code: int
    timestamp: datetime


# ===== Health Check Models =====

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str
    timestamp: datetime
    components: Optional[Dict[str, str]] = None


class ComponentStatus(BaseModel):
    """Component status"""
    name: str
    status: str  # healthy, unhealthy, degraded
    message: Optional[str] = None

class Severity(str, Enum):
    """Severity levels for recommendations"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ApiResponse(BaseModel):
    """Standard API response wrapper"""
    status: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
