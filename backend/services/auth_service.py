"""
Authentication service for AuditAI
"""

from datetime import datetime, timedelta
from typing import Optional, Dict
import jwt
import hashlib
from utils.logger import get_logger

logger = get_logger(__name__)

"""
    Future plan: Refresh Token set up
"""

class AuthService:
    """Authentication Service"""

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        """
        Initialize auth service
        
        Args:
            secret_key: Secret key for JWT signing
            algorithm: JWT algorithm
        """

        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, subject: str, expires_delta: Optional[timedelta] = None, additional_claims: Optional[Dict] = None) -> str :
        """
        Create JWT access token
        
        Args:
            subject: User ID or subject
            expires_delta: Token expiration time
            additional_claims: Additional JWT claims
        
        Returns:
            JWT token string
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=60)

        to_encode = {
            "sub": subject,
            "exp": expire,
            "iat": datetime.utcnow()
        }

        if additional_claims:
            to_encode.update(additional_claims)

        try:
            encoded_jwt = jwt.encode (
                to_encode,
                self.secret_key,
                self.algorithm
            )

            logger.info(f"Access token creted for subject: {subject}")
            return encoded_jwt
        
        except Exception as e:
            logger.error(f"Failed to create access token: {str(e)}")
            raise
    
    def verify_token(self, token: str) -> Dict:
        """
        Verify JWT token
        
        Args:
            token: JWT token string
        
        Returns:
            Decoded token payload
        
        Raises:
            jwt.InvalidTokenError if token is invalid
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            raise jwt.InvalidTokenError("Token has expired")
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            raise 

    def hash_password(self, password: str) -> str:
        """
        Hash password using SHA-256
        
        Args:
            password: Plain text password
        
        Returns:
            Hashed password
        """

        return hashlib.sha224(password.encode()).hexdigest()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify password against hash
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password
        
        Returns:
            True if passwords match
        """

        return self.hash_password(plain_password) == hashed_password