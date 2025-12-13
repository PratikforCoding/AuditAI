"""
Main API endpoints
Updated with MongoDB database operations
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
from typing import Optional
import uuid
import logging
from backend.schemas import (
    UserCreateRequest, UserLoginRequest, AnalysisRequest,
    UserResponse, SuccessResponse, ErrorResponse, HealthCheckResponse
)
from backend.services.encryption import EncryptionService
from backend.services.auth import AuthService
from backend.models.repositories import (
    UserRepository, AnalysisRepository, AuditReportRepository,
    CostAnalysisRepository, SubscriptionRepository
)
from backend.models.db_models import UserDB, UserAnalysisDB
from backend.config.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# Security
security = HTTPBearer()


# ===== HEALTH CHECK =====

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    from backend.config.database import DatabaseConnection
    
    db_healthy = DatabaseConnection.health_check()
    
    return HealthCheckResponse(
        status="healthy",
        service=settings.APP_NAME,
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow(),
        components={
            "database": "healthy" if db_healthy else "unhealthy",
            "api": "healthy"
        }
    )


# ===== AUTHENTICATION ENDPOINTS =====

@router.post("/auth/register", response_model=SuccessResponse)
async def register(request: UserCreateRequest):
    """User registration endpoint"""
    try:
        # Check if user already exists
        existing_user = await UserRepository.find_by_email(request.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        password_hash = AuthService.hash_password(request.password)
        
        # Create user
        user_id = str(uuid.uuid4())
        user = UserDB(
            user_id=user_id,
            email=request.email,
            password_hash=password_hash,
            company_name=request.company_name,
            subscription_tier="free",
            created=datetime.utcnow(),
            updated=datetime.utcnow()
        )
        
        # Save to database
        await UserRepository.create(user)
        
        # Generate access token
        access_token = AuthService.create_access_token(
            data={"sub": user.email, "user_id": user_id}
        )
        
        return SuccessResponse(
            status="success",
            data={
                "user_id": user_id,
                "email": request.email,
                "access_token": access_token,
                "token_type": "bearer"
            },
            message="Registration successful. Please add your GCP credentials next.",
            timestamp=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/auth/login", response_model=SuccessResponse)
async def login(request: UserLoginRequest):
    """User login endpoint"""
    try:
        # Find user
        user = await UserRepository.find_by_email(request.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Verify password
        if not AuthService.verify_password(request.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Update last login
        await UserRepository.update_last_login(user.user_id)
        
        # Generate access token
        access_token = AuthService.create_access_token(
            data={"sub": user.email, "user_id": user.user_id}
        )
        
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
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


# ===== GCP CREDENTIALS ENDPOINTS =====

@router.post("/auth/add-gcp-credentials", response_model=SuccessResponse)
async def add_gcp_credentials(
    credentials_request: dict,
    token: str = Depends(security)
):
    """Add GCP credentials to user account"""
    try:
        # Verify token and get user
        payload = AuthService.verify_token(token.credentials)
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Get user from database
        user = await UserRepository.find_by_id(user_id)
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
        encrypted_credentials = EncryptionService.encrypt(service_account_json)
        
        # Update user with encrypted credentials
        await UserRepository.add_gcp_credentials(
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
        logger.error(f"Add credentials error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add credentials"
        )


# ===== USER ENDPOINTS =====

@router.get("/users/me", response_model=SuccessResponse)
async def get_current_user(token: str = Depends(security)):
    """Get current user information"""
    try:
        # Verify token
        payload = AuthService.verify_token(token.credentials)
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Get user from database
        user = await UserRepository.find_by_id(user_id)
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
                "created": user.created
            },
            timestamp=datetime.utcnow()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get user error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user"
        )


# ===== ANALYSIS ENDPOINTS =====

@router.post("/agent/analyze", response_model=SuccessResponse)
async def analyze_infrastructure(
    request: AnalysisRequest,
    token: str = Depends(security)
):
    """Run infrastructure analysis"""
    try:
        # Verify token
        payload = AuthService.verify_token(token.credentials)
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Get user
        user = await UserRepository.find_by_id(user_id)
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
        decrypted_creds = EncryptionService.decrypt(user.gcp_credentials)
        
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
            created=datetime.utcnow(),
            updated=datetime.utcnow(),
            status="completed"
        )
        
        # Save analysis to database
        await AnalysisRepository.create(analysis)
        
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
        logger.error(f"Analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Analysis failed"
        )


@router.get("/agent/analyses", response_model=SuccessResponse)
async def get_user_analyses(
    limit: int = 10,
    token: str = Depends(security)
):
    """Get user's analysis history"""
    try:
        # Verify token
        payload = AuthService.verify_token(token.credentials)
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Get analyses from database
        analyses = await AnalysisRepository.find_by_user_id(user_id, limit)
        
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
        logger.error(f"Get analyses error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch analyses"
        )


# ===== REPORTS ENDPOINTS =====

@router.get("/reports", response_model=SuccessResponse)
async def get_user_reports(
    limit: int = 10,
    token: str = Depends(security)
):
    """Get user's audit reports"""
    try:
        # Verify token
        payload = AuthService.verify_token(token.credentials)
        user_id = payload.get("user_id")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Get reports from database
        reports = await AuditReportRepository.find_by_user_id(user_id, limit)
        
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
        logger.error(f"Get reports error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch reports"
        )