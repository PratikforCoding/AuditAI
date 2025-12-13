"""
Authentication Service - JWT + Password Hashing
FIXED for Pydantic v2 and bcrypt
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
import jwt
import logging
from passlib.context import CryptContext

from backend.config.settings import settings

logger = logging.getLogger(__name__)

# Bcrypt context for secure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication service for JWT and password management"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password using bcrypt (secure)
        
        Args:
            password: Plain text password
        
        Returns:
            Hashed password
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify password against bcrypt hash
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password from database
        
        Returns:
            True if password matches
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT access token
        
        Args:
            data: Data to encode (must include 'sub' and 'user_id')
            expires_delta: Token expiration time
        
        Returns:
            JWT token string
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                hours=settings.ACCESS_TOKEN_EXPIRE_HOURS
            )
        
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        
        try:
            encoded_jwt = jwt.encode(
                to_encode,
                settings.SECRET_KEY,
                algorithm=settings.ALGORITHM
            )
            logger.info(f"✅ JWT token created for user: {data.get('user_id')}")
            return encoded_jwt
        except Exception as e:
            logger.error(f"❌ Failed to create JWT token: {e}")
            raise
    
    @staticmethod
    def verify_token(token: str) -> Dict:
        """
        Verify JWT token and return payload
        
        Args:
            token: JWT token string
        
        Returns:
            Decoded token payload with user_id and email
        
        Raises:
            jwt.ExpiredSignatureError: Token expired
            jwt.InvalidTokenError: Invalid token
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            
            user_id = payload.get("user_id")
            if not user_id:
                raise jwt.InvalidTokenError("Token missing user_id")
            
            logger.info(f"✅ Token verified for user: {user_id}")
            return payload
        
        except jwt.ExpiredSignatureError:
            logger.warning("⚠️ Token has expired")
            raise
        except jwt.InvalidTokenError as e:
            logger.error(f"❌ Invalid token: {e}")
            raise
