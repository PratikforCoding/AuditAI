"""
Authentication middleware
Validates JWT tokens and extracts user information
"""

import logging
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import jwt
from datetime import datetime, timedelta
from backend.config.settings import settings
from backend.utils.logger import get_logger
from backend.utils.encryption import CredentialEncryption

logger = get_logger(__name__)
security = HTTPBearer()


class JWTHandler:
    """Handle JWT token creation and validation"""
    
    @staticmethod
    def create_access_token(
        subject: str,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT access token
        
        Args:
            subject: User ID to encode in token
            expires_delta: Token expiration time
        
        Returns:
            Encoded JWT token
        """
        if expires_delta is None:
            expires_delta = timedelta(hours=24)
        
        expire = datetime.utcnow() + expires_delta
        to_encode = {"sub": subject, "exp": expire}
        
        try:
            encoded_jwt = jwt.encode(
                to_encode,
                settings.SECRET_KEY,
                algorithm=settings.ALGORITHM
            )
            logger.info(f"JWT token created for user: {subject}")
            return encoded_jwt
        except Exception as e:
            logger.error(f"Failed to create JWT token: {str(e)}")
            raise

    @staticmethod
    def verify_token(token: str) -> str:
        """
        Verify JWT token and extract user_id
        
        Args:
            token: JWT token string
        
        Returns:
            User ID from token
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("sub")
            
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: no user_id"
                )
            
            logger.info(f"Token verified for user: {user_id}")
            return user_id
        
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )


async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security)
) -> str:
    """
    Extract and validate user from JWT token
    Used as dependency in protected endpoints
    
    Args:
        credentials: HTTP Bearer token
    
    Returns:
        User ID
    """
    try:
        token = credentials.credentials
        user_id = JWTHandler.verify_token(token)
        return user_id
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )


async def get_user_gcp_credentials(
    user_id: str = Depends(get_current_user)
) -> dict:
    """
    Get decrypted GCP credentials for authenticated user
    
    Args:
        user_id: Current authenticated user
    
    Returns:
        Decrypted GCP credentials
    """
    try:
        from backend.models.database import db
        
        user = db.User.find_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.get('gcp_credentials'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User hasn't configured GCP credentials yet"
            )
        
        encryptor = CredentialEncryption()
        credentials = encryptor.decrypt(user['gcp_credentials'])
        
        logger.info(f"GCP credentials retrieved for user: {user_id}")
        return credentials
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve credentials for {user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve credentials"
        )