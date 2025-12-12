"""
Authentication API endpoints
- Register user
- Login user
- Add GCP credentials
- Verify credentials
"""

import logging
import uuid
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime, timedelta
from backend.models.schemas import (
    UserCreateRequest,
    UserLoginRequest,
    AddCredentialsRequest
)
from backend.middleware.auth import JWTHandler, get_current_user
from backend.utils.encryption import PasswordEncryption, CredentialEncryption
from backend.utils.logger import get_logger
from backend.gcp_client import GCPClient

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post("/register", response_model=dict)
async def register_user(request: UserCreateRequest):
    """
    Register new user account
    
    Args:
        request: User registration details
    
    Returns:
        Success message with user_id
    """
    try:
        logger.info(f"Registration attempt for: {request.email}")
        
        from backend.models.database import db
        
        existing_user = db.User.find_by_email(request.email)
        if existing_user:
            logger.warning(f"Registration failed: email already registered: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        user_id = str(uuid.uuid4())
        password_hash = PasswordEncryption.hash_password(request.password)
        
        user_data = {
            "id": user_id,
            "email": request.email,
            "password_hash": password_hash,
            "company_name": request.company_name,
            "gcp_project_id": None,
            "gcp_credentials": None,
            "created": datetime.utcnow().isoformat(),
            "last_login": None,
            "subscription_tier": "free",
            "is_active": True
        }
        
        db.User.save(user_data)
        logger.info(f"User registered successfully: {user_id}")
        
        return {
            "status": "success",
            "user_id": user_id,
            "email": request.email,
            "message": "Registration successful. Please log in."
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
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
    """
    try:
        logger.info(f"Login attempt for: {request.email}")
        
        from backend.models.database import db
        
        user = db.User.find_by_email(request.email)
        if not user:
            logger.warning(f"Login failed: user not found: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not PasswordEncryption.verify_password(request.password, user['password_hash']):
            logger.warning(f"Login failed: invalid password for: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not user.get('is_active', False):
            logger.warning(f"Login failed: account inactive: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        token = JWTHandler.create_access_token(subject=user['id'])
        
        db.User.update_last_login(user['id'])
        
        logger.info(f"User logged in successfully: {user['id']}")
        
        return {
            "status": "success",
            "token": token,
            "user_id": user['id'],
            "email": user['email'],
            "has_gcp_credentials": bool(user.get('gcp_credentials'))
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/add-gcp-credentials")
async def add_gcp_credentials(
    request: AddCredentialsRequest,
    user_id: str = Depends(get_current_user)
):
    """
    User uploads their GCP credentials
    Validates and encrypts before storing
    
    Args:
        request: GCP project details and credentials
        user_id: Current authenticated user
    
    Returns:
        Success message
    """
    try:
        logger.info(f"Adding GCP credentials for user: {user_id}")
        
        from backend.models.database import db
        
        try:
            gcp_client = GCPClient(request.project_id)
            if not gcp_client.verify_credentials():
                logger.warning(f"Invalid GCP credentials for user: {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="GCP credentials are invalid or insufficient"
                )
        except Exception as e:
            logger.error(f"GCP validation failed for user {user_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to validate GCP credentials: {str(e)}"
            )
        
        encryptor = CredentialEncryption()
        encrypted_creds = encryptor.encrypt({
            "project_id": request.project_id,
            "service_account_json": request.service_account_json,
            "api_key": request.api_key
        })
        
        db.User.add_gcp_credentials(
            user_id=user_id,
            project_id=request.project_id,
            encrypted_credentials=encrypted_creds
        )
        
        logger.info(f"GCP credentials saved for user: {user_id}")
        
        return {
            "status": "success",
            "message": "GCP credentials saved successfully",
            "project_id": request.project_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to add credentials for {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save credentials"
        )


@router.get("/verify-credentials")
async def verify_credentials(user_id: str = Depends(get_current_user)):
    """
    Verify that user's GCP credentials are valid
    
    Args:
        user_id: Current authenticated user
    
    Returns:
        Credential status
    """
    try:
        logger.info(f"Verifying credentials for user: {user_id}")
        
        from backend.models.database import db
        
        user = db.User.find_by_id(user_id)
        
        if not user or not user.get('gcp_credentials'):
            return {
                "has_credentials": False,
                "is_valid": False,
                "message": "No GCP credentials configured"
            }
        
        encryptor = CredentialEncryption()
        try:
            creds = encryptor.decrypt(user['gcp_credentials'])
            gcp_client = GCPClient(creds['project_id'])
            is_valid = gcp_client.verify_credentials()
        except:
            is_valid = False
        
        logger.info(f"Credentials verified for user: {user_id}, valid: {is_valid}")
        
        return {
            "has_credentials": True,
            "is_valid": is_valid,
            "project_id": user.get('gcp_project_id')
        }
    
    except Exception as e:
        logger.error(f"Verification failed for {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Verification failed"
        )


@router.get("/me")
async def get_current_user_info(user_id: str = Depends(get_current_user)):
    """
    Get current user information
    
    Args:
        user_id: Current authenticated user
    
    Returns:
        User details
    """
    try:
        from backend.models.database import db
        
        user = db.User.find_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {
            "user_id": user['id'],
            "email": user['email'],
            "company_name": user.get('company_name'),
            "subscription_tier": user.get('subscription_tier'),
            "has_gcp_credentials": bool(user.get('gcp_credentials')),
            "created": user.get('created')
        }
    
    except Exception as e:
        logger.error(f"Failed to get user info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user information"
        )