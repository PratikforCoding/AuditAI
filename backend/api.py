"""
Main API endpoints - FIXED VERSION
Uses proper Repository pattern instead of db.User
Removes async/await where not needed
"""

from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime
from typing import Optional
import uuid
import logging

from backend.models.schemas import (
    UserCreateRequest, UserLoginRequest, AnalysisRequest,
    UserResponse, SuccessResponse, HealthCheckResponse
)
from backend.services.auth_service import AuthService
from backend.utils.encryption import CredentialEncryption
from backend.middleware.auth import get_current_user, get_current_active_user
from backend.models.repositories import (
    UserRepository,
    AnalysisRepository,
    AuditReportRepository,
    CostAnalysisRepository
)
from backend.models.db_models import UserDB, UserAnalysisDB
from backend.config.settings import settings
from backend.config.database import DatabaseConnection

logger = logging.getLogger(__name__)
router = APIRouter()


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health", response_model=HealthCheckResponse)
def health_check():  # ✅ FIXED: Removed async (not needed)
    """
    Health check endpoint
    Verifies API and database connectivity
    """
    db_healthy = DatabaseConnection.health_check()
    
    return HealthCheckResponse(
        status="healthy" if db_healthy else "degraded",
        service=settings.APP_NAME,
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow(),
        components={
            "database": "healthy" if db_healthy else "unhealthy",
            "api": "healthy"
        }
    )


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@router.post("/auth/register", response_model=SuccessResponse)
def register(request: UserCreateRequest):  # ✅ FIXED: Removed async
    """
    User registration endpoint
    
    Args:
        request: User registration details
    
    Returns:
        Success response with JWT token
    """
    try:
        # ✅ FIXED: Use Repository pattern (not db.User)
        existing_user = UserRepository.find_by_email(request.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # ✅ FIXED: Use unified AuthService
        password_hash = AuthService.hash_password(request.password)
        
        # Create user
        user_id = str(uuid.uuid4())
        user = UserDB(
            user_id=user_id,
            email=request.email,
            password_hash=password_hash,
            company_name=request.company_name,
            subscription_tier="free",
            is_active=True,
            created=datetime.utcnow(),
            updated=datetime.utcnow()
        )
        
        # Save to database
        UserRepository.create(user)
        
        # Generate access token
        access_token = AuthService.create_access_token(
            user_id=user_id,
            email=user.email
        )
        
        logger.info(f"✅ User registered: {user_id}")
        
        return SuccessResponse(
            status="success",
            data={
                "user_id": user_id,
                "email": request.email,
                "access_token": access_token,
                "token_type": "bearer"
            },
            message="Registration successful. Please add GCP credentials next.",
            timestamp=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/auth/login", response_model=SuccessResponse)
def login(request: UserLoginRequest):  # ✅ FIXED: Removed async
    """
    User login endpoint
    
    Args:
        request: Email and password
    
    Returns:
        Success response with JWT token
    """
    try:
        # ✅ FIXED: Use Repository pattern
        user = UserRepository.find_by_email(request.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # ✅ FIXED: Use unified AuthService
        if not AuthService.verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Check if active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        # Update last login
        UserRepository.update_last_login(user.user_id)
        
        # Generate access token
        access_token = AuthService.create_access_token(
            user_id=user.user_id,
            email=user.email
        )
        
        logger.info(f"✅ User logged in: {user.user_id}")
        
        return SuccessResponse(
            status="success",
            data={
                "user_id": user.user_id,
                "email": user.email,
                "company_name": user.company_name,
                "access_token": access_token,
                "token_type": "bearer",
                "has_gcp_credentials": user.gcp_credentials is not None
            },
            message="Login successful",
            timestamp=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


# ============================================================================
# GCP CREDENTIALS ENDPOINTS
# ============================================================================

@router.post("/auth/add-gcp-credentials", response_model=SuccessResponse)
def add_gcp_credentials(
    credentials_request: dict,
    user_id: str = Depends(get_current_user)  # ✅ FIXED: Use middleware
):
    """
    Add GCP credentials to user account
    
    Args:
        credentials_request: GCP project ID and service account JSON
        user_id: Extracted from JWT token
    
    Returns:
        Success response
    """
    try:
        # Get user from database
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Extract and validate credentials
        project_id = credentials_request.get("project_id")
        service_account_json = credentials_request.get("service_account_json")
        
        if not project_id or not service_account_json:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing project_id or service_account_json"
            )
        
        # Encrypt credentials
        encryptor = CredentialEncryption()
        encrypted_credentials = encryptor.encrypt({
            "project_id": project_id,
            "service_account_json": service_account_json
        })
        
        # Update user with encrypted credentials
        UserRepository.add_gcp_credentials(
            user_id,
            project_id,
            encrypted_credentials
        )
        
        logger.info(f"✅ GCP credentials added for user: {user_id}")
        
        return SuccessResponse(
            status="success",
            data={"project_id": project_id},
            message="GCP credentials added successfully",
            timestamp=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Add credentials error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add credentials"
        )


# ============================================================================
# USER ENDPOINTS
# ============================================================================

@router.get("/users/me", response_model=SuccessResponse)
def get_current_user_endpoint(
    user_id: str = Depends(get_current_user)  # ✅ FIXED: Use middleware
):
    """
    Get current user information
    
    Args:
        user_id: Extracted from JWT token
    
    Returns:
        User information
    """
    try:
        # Get user from database
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return SuccessResponse(
            status="success",
            data={
                "user_id": user.user_id,
                "email": user.email,
                "company_name": user.company_name,
                "subscription_tier": user.subscription_tier,
                "has_gcp_credentials": user.gcp_credentials is not None,
                "is_active": user.is_active,
                "created": user.created
            },
            timestamp=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Get user error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user"
        )


# ============================================================================
# ANALYSIS ENDPOINTS
# ============================================================================

@router.post("/agent/analyze", response_model=SuccessResponse)
def analyze_infrastructure(
    request: AnalysisRequest,
    user_id: str = Depends(get_current_user)  # ✅ FIXED: Use middleware
):
    """
    Run infrastructure analysis
    
    Args:
        request: Analysis request with query and days
        user_id: Extracted from JWT token
    
    Returns:
        Analysis result
    """
    try:
        # Get user
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Validate GCP credentials
        if not user.gcp_credentials or not user.gcp_project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="GCP credentials not configured. Add credentials first."
            )
        
        # Decrypt credentials
        encryptor = CredentialEncryption()
        decrypted_creds = encryptor.decrypt(user.gcp_credentials)
        
        # TODO: Call Gemini AI for analysis
        # For now, return mock response
        
        analysis_id = str(uuid.uuid4())
        analysis = UserAnalysisDB(
            analysis_id=analysis_id,
            user_id=user_id,
            project_id=user.gcp_project_id,
            query=request.query,
            result={
                "status": "success",
                "analysis": "Infrastructure analysis completed",
                "recommendations": [],
                "total_savings": 0
            },
            cost_savings=0,
            execution_time=None,
            created=datetime.utcnow(),
            updated=datetime.utcnow(),
            status="completed"
        )
        
        # Save analysis to database
        AnalysisRepository.create(analysis)
        
        logger.info(f"✅ Analysis created: {analysis_id}")
        
        return SuccessResponse(
            status="success",
            data={
                "analysis_id": analysis_id,
                "query": request.query,
                "result": analysis.result
            },
            message="Analysis completed successfully",
            timestamp=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Analysis failed"
        )


@router.get("/agent/analyses", response_model=SuccessResponse)
def get_user_analyses(
    limit: int = 10,
    user_id: str = Depends(get_current_user)  # ✅ FIXED: Use middleware
):
    """
    Get user's analysis history
    
    Args:
        limit: Number of analyses to return
        user_id: Extracted from JWT token
    
    Returns:
        List of analyses
    """
    try:
        # Get analyses from database
        analyses = AnalysisRepository.find_by_user_id(user_id, limit)
        
        return SuccessResponse(
            status="success",
            data={
                "analyses": [a.dict() for a in analyses],
                "count": len(analyses)
            },
            timestamp=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Get analyses error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch analyses"
        )


# ============================================================================
# REPORTS ENDPOINTS
# ============================================================================

@router.get("/reports", response_model=SuccessResponse)
def get_user_reports(
    limit: int = 10,
    user_id: str = Depends(get_current_user)  # ✅ FIXED: Use middleware
):
    """
    Get user's audit reports
    
    Args:
        limit: Number of reports to return
        user_id: Extracted from JWT token
    
    Returns:
        List of audit reports
    """
    try:
        # Get reports from database
        reports = AuditReportRepository.find_by_user_id(user_id, limit)
        
        return SuccessResponse(
            status="success",
            data={
                "reports": [r.dict() for r in reports],
                "count": len(reports)
            },
            timestamp=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Get reports error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch reports"
        )