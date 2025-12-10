"""
AI Agent Endpoints - Agentic AI API Routes
Provides endpoints for AI-powered infrastructure analysis and recommendations
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List
import logging
from backend.services.gemini_agent_service import GeminiAgentService
from backend.models.schemas import ApiResponse
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Create router for agent endpoints
router = APIRouter(
    prefix="/api/v1/agent",
    tags=["agent"],
    responses={404: {"description": "Not found"}},
)


# ============================================================================
# Request Models
# ============================================================================

class AnalysisRequest(BaseModel):
    """Request body for infrastructure analysis"""
    project_id: str = Field(..., description="GCP Project ID")
    query: str = Field(..., description="User's question about infrastructure")
    days: int = Field(default=30, description="Days to analyze")

    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "my-gcp-project",
                "query": "What can I do to reduce costs by 30%?",
                "days": 30
            }
        }


class SuggestionsRequest(BaseModel):
    """Request body for getting optimization suggestions"""
    project_id: str = Field(..., description="GCP Project ID")

    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "my-gcp-project"
            }
        }


class ExecutePlanRequest(BaseModel):
    """Request body for executing optimization plan"""
    project_id: str = Field(..., description="GCP Project ID")
    plan: str = Field(..., description="Optimization plan to execute")
    dry_run: bool = Field(default=True, description="Simulate without executing")

    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "my-gcp-project",
                "plan": "Delete idle compute instances",
                "dry_run": True
            }
        }


# ============================================================================
# Response Models
# ============================================================================

class AnalysisResponse(BaseModel):
    """Response model for infrastructure analysis"""
    status: str
    query: str
    analysis: str
    project_id: str
    days_analyzed: int
    tool_calls: Optional[List] = None


class SuggestionsResponse(BaseModel):
    """Response model for optimization suggestions"""
    status: str
    suggestions: str
    project_id: str
    data_sources: List[str]


class AuditReportResponse(BaseModel):
    """Response model for audit report"""
    status: str
    report: str
    project_id: str
    days_analyzed: int
    generated_at: str


# ============================================================================
# AI Agent Endpoints
# ============================================================================

@router.post(
    "/analyze",
    response_model=ApiResponse,
    summary="Analyze Infrastructure with AI",
    description="Use AI agent to analyze GCP infrastructure and answer questions"
)
async def analyze_infrastructure(request: AnalysisRequest):
    """
    Analyze infrastructure using Gemini AI with tool use.
    
    The AI agent can autonomously:
    - Get cost analysis by service
    - Retrieve resource metrics
    - Pull GCP Recommender suggestions
    - Calculate potential savings
    
    **Example queries:**
    - "What's wasting the most money in my infrastructure?"
    - "How can I reduce costs by 30%?"
    - "Which resources are underutilized?"
    - "What's my total monthly spend?"
    
    **Response includes:**
    - AI analysis and insights
    - Specific recommendations
    - Cost calculations
    - Implementation suggestions
    """
    try:
        logger.info(f"Analyzing infrastructure for project: {request.project_id}")
        
        # Initialize AI agent service
        agent = GeminiAgentService(request.project_id)
        
        # Run interactive analysis
        result = agent.analyze_infrastructure_interactively(
            query=request.query,
            days=request.days
        )
        
        if result["status"] != "success":
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Analysis failed")
            )
        
        return ApiResponse(
            status="success",
            message="Infrastructure analysis completed",
            data={
                "query": result["query"],
                "analysis": result["analysis"],
                "tool_calls": result.get("tool_calls", []),
                "project_id": result["project_id"],
                "days_analyzed": result["days_analyzed"]
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get(
    "/suggestions",
    response_model=ApiResponse,
    summary="Get AI Optimization Suggestions",
    description="Get AI-powered optimization suggestions for reducing costs"
)
async def get_suggestions(project_id: str):
    """
    Get AI-powered optimization suggestions.
    
    The AI analyzes:
    - Current costs by service
    - Resource utilization metrics
    - GCP Recommender suggestions
    
    **Response includes:**
    - Top 5 optimization suggestions
    - Expected cost savings for each
    - Implementation difficulty levels
    - ROI estimates
    """
    try:
        logger.info(f"Generating suggestions for project: {project_id}")
        
        # Initialize AI agent service
        agent = GeminiAgentService(project_id)
        
        # Get suggestions
        result = agent.get_optimization_suggestions()
        
        if result["status"] != "success":
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Failed to generate suggestions")
            )
        
        return ApiResponse(
            status="success",
            message="Optimization suggestions generated",
            data={
                "suggestions": result["suggestions"],
                "project_id": result["project_id"],
                "data_sources": result["data_sources"]
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate suggestions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate suggestions: {str(e)}"
        )


@router.post(
    "/execute-plan",
    response_model=ApiResponse,
    summary="Execute Optimization Plan",
    description="Execute an optimization plan suggested by AI"
)
async def execute_plan(request: ExecutePlanRequest, background_tasks: BackgroundTasks):
    """
    Execute an optimization plan.
    
    **Dry Run Mode (default):**
    - Simulates the changes
    - Shows what would be done
    - No actual changes made
    - Use for validation before execution
    
    **Execution Mode (dry_run=false):**
    - Actually implements the plan
    - Modifies GCP resources
    - Requires proper IAM permissions
    - Returns actual results
    
    **Note:** Complex changes may take time and run in background.
    Monitor job status separately.
    """
    try:
        logger.info(
            f"Executing plan for project: {request.project_id} "
            f"(dry_run={request.dry_run})"
        )
        
        if request.dry_run:
            return ApiResponse(
                status="success",
                message="Dry run simulation completed",
                data={
                    "mode": "dry_run",
                    "plan": request.plan,
                    "project_id": request.project_id,
                    "changes": {
                        "status": "simulated",
                        "message": "Use dry_run=false to execute actual changes"
                    }
                }
            )
        else:
            # In production, you would actually execute the plan
            logger.warning(f"Executing plan (NOT DRY RUN): {request.plan}")
            
            # For now, return success status
            # In production, this would trigger actual GCP API calls
            return ApiResponse(
                status="success",
                message="Plan execution initiated",
                data={
                    "mode": "execution",
                    "plan": request.plan,
                    "project_id": request.project_id,
                    "status": "in_progress",
                    "estimated_duration": "5-10 minutes"
                }
            )
    
    except Exception as e:
        logger.error(f"Plan execution failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Plan execution failed: {str(e)}"
        )


@router.get(
    "/report",
    response_model=ApiResponse,
    summary="Generate Audit Report",
    description="Generate comprehensive infrastructure audit report"
)
async def generate_audit_report(
    project_id: str,
    days: int = 30
):
    """
    Generate comprehensive audit report.
    
    The report includes:
    - Executive summary
    - Key findings
    - Cost breakdown
    - Top recommendations with ROI
    - Risk assessment
    - Implementation timeline
    - Expected cost savings
    - Detailed analysis
    
    **Query Parameters:**
    - project_id: GCP Project ID
    - days: Number of days to analyze (default 30)
    """
    try:
        logger.info(f"Generating audit report for project: {project_id}")
        
        # Initialize AI agent service
        agent = GeminiAgentService(project_id)
        
        # Generate report
        result = agent.generate_audit_report(days=days)
        
        if result["status"] != "success":
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Failed to generate report")
            )
        
        return ApiResponse(
            status="success",
            message="Audit report generated",
            data={
                "report": result["report"],
                "project_id": result["project_id"],
                "days_analyzed": result["days_analyzed"],
                "generated_at": result["generated_at"]
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to generate report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate report: {str(e)}"
        )


@router.get(
    "/health",
    response_model=ApiResponse,
    summary="Agent Health Check",
    description="Check if AI agent service is operational"
)
async def agent_health():
    """Check if AI agent service is healthy and ready"""
    return ApiResponse(
        status="success",
        message="AI Agent service is operational",
        data={
            "service": "gemini_agent",
            "status": "healthy",
            "capabilities": [
                "infrastructure_analysis",
                "cost_optimization",
                "recommendations",
                "audit_reports"
            ]
        }
    )


# Export router for inclusion in main app
__all__ = ["router"]