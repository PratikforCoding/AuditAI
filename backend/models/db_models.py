"""
Database models for MongoDB collections
Defines the structure of documents in each collection
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class UserDB(BaseModel):
    """User document model"""
    user_id: str
    email: str
    password_hash: str
    company_name: Optional[str] = None
    gcp_project_id: Optional[str] = None
    gcp_credentials: Optional[str] = None  # Encrypted
    subscription_tier: str = "free"
    is_active: bool = True
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@company.com",
                "password_hash": "$2b$12$...",
                "company_name": "ACME Corp",
                "gcp_project_id": "acme-gcp-project",
                "gcp_credentials": "gAAAAABmDy3e...",
                "subscription_tier": "pro",
                "is_active": True,
                "created": "2025-12-13T11:42:00Z",
                "last_login": "2025-12-13T11:42:00Z"
            }
        }


class RecommendationDB(BaseModel):
    """Recommendation sub-document"""
    id: str
    title: str
    description: str
    category: str  # compute, storage, database, networking
    resource_type: str
    severity: str  # Critical, High, Medium, Low
    estimated_savings: Optional[float] = None
    implementation_time: str  # Quick, Medium, Long
    confidence: float  # 0.0 to 1.0


class AnalysisResultDB(BaseModel):
    """Analysis result sub-document"""
    status: str
    query: str
    analysis: str
    recommendations: List[RecommendationDB] = []
    total_cost_potential_savings: Optional[float] = None
    project_id: str
    days_analyzed: int
    generated_at: datetime


class UserAnalysisDB(BaseModel):
    """User analysis document model"""
    analysis_id: str
    user_id: str
    project_id: str
    query: str
    result: Dict[str, Any]
    cost_savings: Optional[float] = None
    execution_time: Optional[float] = None  # seconds
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)
    status: str = "completed"  # pending, processing, completed, failed
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_id": "analysis-uuid-123",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "project_id": "acme-gcp-project",
                "query": "How can I reduce costs by 30%?",
                "result": {
                    "analysis": "Based on your GCP account...",
                    "recommendations": [],
                    "total_savings": 50000
                },
                "cost_savings": 50000,
                "created": "2025-12-13T11:42:00Z"
            }
        }


class AuditReportDB(BaseModel):
    """Audit report document model"""
    report_id: str
    user_id: str
    project_id: str
    title: str
    executive_summary: str
    current_state: str
    findings: List[str]
    recommendations: List[str]
    cost_analysis: Dict[str, Any]
    priority_actions: List[str]
    estimated_roi: Optional[float] = None
    timeframe: str  # Quick wins, Medium-term, Strategic
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)
    pdf_url: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_id": "report-uuid-456",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "project_id": "acme-gcp-project",
                "title": "Infrastructure Audit Report - Dec 2025",
                "executive_summary": "Your GCP infrastructure shows...",
                "current_state": "Monthly spend: $45,000...",
                "findings": ["Idle compute instances", "Oversized VMs"],
                "recommendations": ["Terminate idle instances"],
                "cost_analysis": {},
                "priority_actions": ["Action 1"],
                "estimated_roi": 150,
                "timeframe": "Quick wins"
            }
        }


class CostBreakdownDB(BaseModel):
    """Cost breakdown sub-document"""
    service: str
    current_cost: float
    projected_cost: Optional[float] = None
    potential_savings: Optional[float] = None
    percentage: float


class CostAnalysisDB(BaseModel):
    """Cost analysis document model"""
    cost_analysis_id: str
    user_id: str
    project_id: str
    total_current_cost: float
    total_projected_cost: Optional[float] = None
    total_potential_savings: Optional[float] = None
    breakdown: List[CostBreakdownDB]
    trend: str  # Increasing, Stable, Decreasing
    analysis_date: datetime = Field(default_factory=datetime.utcnow)
    created: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "cost_analysis_id": "cost-analysis-789",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "project_id": "acme-gcp-project",
                "total_current_cost": 45000,
                "total_projected_cost": 38000,
                "total_potential_savings": 7000,
                "breakdown": [],
                "trend": "Increasing"
            }
        }


class SubscriptionDB(BaseModel):
    """Subscription document model"""
    subscription_id: str
    user_id: str
    plan: str  # free, pro, enterprise
    billing_date: datetime
    amount: float
    status: str  # active, cancelled, past_due
    features: Dict[str, Any]
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: datetime = Field(default_factory=datetime.utcnow)
    renewal_date: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "subscription_id": "sub-uuid-001",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "plan": "pro",
                "billing_date": "2025-01-13T00:00:00Z",
                "amount": 99.99,
                "status": "active",
                "features": {
                    "analyses_per_month": 100,
                    "api_calls": 10000,
                    "reports": "unlimited"
                }
            }
        }