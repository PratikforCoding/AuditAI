"""
Authentication API endpoints - FIXED VERSION
Uses proper Repository pattern and JWT middleware
"""

import logging
import uuid
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime

from backend.models.schemas import (
    UserCreateRequest,
    UserLoginRequest,
    AddCredentialsRequest
)
from backend.models.repositories import UserRepository
from backend.models.db_models import UserDB
from backend.middleware.auth import get_current_user, get_current_active_user
from backend.services.auth_service import AuthService
from backend.utils.encryption import CredentialEncryption
from backend.gcp_client import GCPClient

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


# ============================================================================
# PUBLIC ENDPOINTS (No Authentication Required)
# ============================================================================

@router.post("/register", response_model=dict)
async def register_user(request: UserCreateRequest):
    """
    Register new user account
    
    Args:
        request: User registration details (email, password, company_name)
    
    Returns:
        Success message with user_id and JWT token
    
    Example:
        POST /api/v1/auth/register
        {
            "email": "user@company.com",
            "password": "SecurePass123!",
            "company_name": "ACME Corp"
        }
    """
    try:
        logger.info(f"📝 Registration attempt: {request.email}")
        
        # ✅ FIXED: Use Repository pattern
        existing_user = UserRepository.find_by_email(request.email)
        if existing_user:
            logger.warning(f"❌ Email already registered: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Generate user ID
        user_id = str(uuid.uuid4())
        
        # ✅ FIXED: Use unified AuthService with bcrypt
        password_hash = AuthService.hash_password(request.password)
        
        # Create user object
        user = UserDB(
            user_id=user_id,
            email=request.email,
            password_hash=password_hash,
            company_name=request.company_name,
            gcp_project_id=None,
            gcp_credentials=None,
            subscription_tier="free",
            is_active=True,
            created=datetime.utcnow(),
            updated=datetime.utcnow(),
            last_login=None
        )
        
        # Save to database
        UserRepository.create(user)
        logger.info(f"✅ User registered: {user_id}")
        
        # Generate JWT token
        token = AuthService.create_access_token(
            user_id=user_id,
            email=request.email
        )
        
        return {
            "status": "success",
            "user_id": user_id,
            "email": request.email,
            "token": token,
            "token_type": "bearer",
            "message": "Registration successful. Please add GCP credentials next."
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=dict)
async def login_user(request: UserLoginRequest):
    """
    Authenticate user and return JWT token
    
    Args:
        request: Email and password
    
    Returns:
        JWT token and user info
    
    Example:
        POST /api/v1/auth/login
        {
            "email": "user@company.com",
            "password": "SecurePass123!"
        }
    """
    try:
        logger.info(f"🔐 Login attempt: {request.email}")
        
        # ✅ FIXED: Use Repository pattern
        user = UserRepository.find_by_email(request.email)
        if not user:
            logger.warning(f"❌ User not found: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # ✅ FIXED: Use unified AuthService with bcrypt
        if not AuthService.verify_password(request.password, user.password_hash):
            logger.warning(f"❌ Invalid password: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if account is active
        if not user.is_active:
            logger.warning(f"❌ Inactive account: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive. Please contact support."
            )
        
        # Generate JWT token
        token = AuthService.create_access_token(
            user_id=user.user_id,
            email=user.email
        )
        
        # Update last login
        UserRepository.update_last_login(user.user_id)
        
        logger.info(f"✅ User logged in: {user.user_id}")
        
        return {
            "status": "success",
            "token": token,
            "token_type": "bearer",
            "user_id": user.user_id,
            "email": user.email,
            "company_name": user.company_name,
            "has_gcp_credentials": bool(user.gcp_credentials),
            "subscription_tier": user.subscription_tier
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


# ============================================================================
# PROTECTED ENDPOINTS (Require Authentication)
# ============================================================================

@router.post("/add-gcp-credentials")
async def add_gcp_credentials(
    request: AddCredentialsRequest,
    user_id: str = Depends(get_current_user)  # ✅ FIXED: Use middleware
):
    """
    Add GCP credentials to user account
    Validates and encrypts before storing
    
    Args:
        request: GCP project details and service account JSON
        user_id: Automatically extracted from JWT token
    
    Returns:
        Success message
    
    Example:
        POST /api/v1/auth/add-gcp-credentials
        Headers: Authorization: Bearer <jwt_token>
        {
            "project_id": "my-gcp-project",
            "service_account_json": "{...}",
            "api_key": "AIzaSy..."
        }
    """
    try:
        logger.info(f"🔑 Adding GCP credentials for user: {user_id}")
        
        # Validate GCP credentials
        try:
            gcp_client = GCPClient(request.project_id)
            if not gcp_client.verify_credentials():
                logger.warning(f"❌ Invalid GCP credentials: {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="GCP credentials are invalid or lack required permissions"
                )
        except Exception as e:
            logger.error(f"❌ GCP validation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to validate GCP credentials: {str(e)}"
            )
        
        # Encrypt credentials
        encryptor = CredentialEncryption()
        encrypted_creds = encryptor.encrypt({
            "project_id": request.project_id,
            "service_account_json": request.service_account_json,
            "api_key": request.api_key
        })
        
        # ✅ FIXED: Use Repository pattern
        UserRepository.add_gcp_credentials(
            user_id=user_id,
            project_id=request.project_id,
            encrypted_credentials=encrypted_creds
        )
        
        logger.info(f"✅ GCP credentials saved: {user_id}")
        
        return {
            "status": "success",
            "message": "GCP credentials saved successfully",
            "project_id": request.project_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to add credentials: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save credentials"
        )


@router.get("/verify-credentials")
async def verify_credentials(
    user_id: str = Depends(get_current_user)  # ✅ FIXED: Use middleware
):
    """
    Verify that user's GCP credentials are valid
    
    Args:
        user_id: Automatically extracted from JWT token
    
    Returns:
        Credential status and validation result
    
    Example:
        GET /api/v1/auth/verify-credentials
        Headers: Authorization: Bearer <jwt_token>
    """
    try:
        logger.info(f"🔍 Verifying credentials for user: {user_id}")
        
        # ✅ FIXED: Use Repository pattern
        user = UserRepository.find_by_id(user_id)
        
        if not user or not user.gcp_credentials:
            return {
                "status": "no_credentials",
                "has_credentials": False,
                "is_valid": False,
                "message": "No GCP credentials configured"
            }
        
        # Decrypt and validate
        encryptor = CredentialEncryption()
        try:
            creds = encryptor.decrypt(user.gcp_credentials)
            gcp_client = GCPClient(creds['project_id'])
            is_valid = gcp_client.verify_credentials()
        except Exception as e:
            logger.error(f"❌ Credential validation failed: {e}")
            is_valid = False
        
        logger.info(f"✅ Credentials verified: {user_id}, valid: {is_valid}")
        
        return {
            "status": "success",
            "has_credentials": True,
            "is_valid": is_valid,
            "project_id": user.gcp_project_id,
            "message": "Credentials are valid" if is_valid else "Credentials are invalid"
        }
    
    except Exception as e:
        logger.error(f"❌ Verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Verification failed"
        )


@router.get("/me")
async def get_current_user_info(
    user: dict = Depends(get_current_active_user)  # ✅ FIXED: Use middleware
):
    """
    Get current user information from database
    
    Args:
        user: Automatically extracted from JWT and fetched from database
    
    Returns:
        User details
    
    Example:
        GET /api/v1/auth/me
        Headers: Authorization: Bearer <jwt_token>
    """
    try:
        return {
            "status": "success",
            "user": {
                "user_id": user['user_id'],
                "email": user['email'],
                "company_name": user.get('company_name'),
                "subscription_tier": user.get('subscription_tier'),
                "has_gcp_credentials": bool(user.get('gcp_credentials')),
                "is_active": user.get('is_active'),
                "created": user.get('created'),
                "last_login": user.get('last_login')
            }
        }
    
    except Exception as e:
        logger.error(f"❌ Failed to get user info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user information"
        )


@router.delete("/logout")
async def logout_user(
    user_id: str = Depends(get_current_user)  # ✅ FIXED: Use middleware
):
    """
    Logout user (client-side token deletion)
    
    Note: JWT tokens are stateless. Client must delete the token.
    This endpoint is for logging purposes only.
    
    Args:
        user_id: Automatically extracted from JWT token
    
    Returns:
        Logout confirmation
    """
    try:
        logger.info(f"👋 User logged out: {user_id}")
        
        return {
            "status": "success",
            "message": "Logged out successfully. Please delete token on client side."
        }
    
    except Exception as e:
        logger.error(f"❌ Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )