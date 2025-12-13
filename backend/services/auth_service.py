"""
Unified Authentication Service
Consolidates all auth operations: JWT + Password Hashing
Uses bcrypt for secure password hashing
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
import jwt
import logging
from passlib.context import CryptContext
from backend.config.settings import settings

logger = logging.getLogger(__name__)

# Bcrypt context for secure password hashing
# Using bcrypt with truncate_error=False to handle longer passwords
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__truncate_error=False  # Allow passwords longer than 72 bytes
)


class AuthService:
    """
    Unified authentication service
    Handles both JWT tokens and password hashing
    """
    
    # ========================================================================
    # PASSWORD HASHING (Using bcrypt - SECURE)
    # ========================================================================
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password using bcrypt (industry standard, secure)
        
        Args:
            password: Plain text password
        
        Returns:
            Bcrypt hashed password (includes salt automatically)
        
        Example:
            hashed = AuthService.hash_password("MySecurePass123")
        """
        try:
            hashed = pwd_context.hash(password)
            logger.info("Password hashed successfully")
            return hashed
        except Exception as e:
            logger.error(f"Password hashing failed: {e}")
            raise
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify password against bcrypt hash
        
        Args:
            plain_password: Plain text password from user
            hashed_password: Hashed password from database
        
        Returns:
            True if password matches, False otherwise
        
        Example:
            is_valid = AuthService.verify_password("MySecurePass123", hashed)
        """
        try:
            is_valid = pwd_context.verify(plain_password, hashed_password)
            logger.info(f"Password verification: {'success' if is_valid else 'failed'}")
            return is_valid
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False
    
    # ========================================================================
    # JWT TOKEN OPERATIONS
    # ========================================================================
    
    @staticmethod
    def create_access_token(
        user_id: str,
        email: str,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT access token
        
        Args:
            user_id: User's unique ID
            email: User's email address
            expires_delta: Token expiration time (default: 24 hours)
        
        Returns:
            JWT token string
        
        Example:
            token = AuthService.create_access_token(
                user_id="uuid-123",
                email="user@example.com"
            )
        """
        try:
            # Set expiration
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(
                    hours=settings.ACCESS_TOKEN_EXPIRE_HOURS
                )
            
            # Create payload
            payload = {
                "sub": email,           # Subject (email)
                "user_id": user_id,     # User ID
                "exp": expire,          # Expiration
                "iat": datetime.utcnow()  # Issued at
            }
            
            # Encode JWT
            token = jwt.encode(
                payload,
                settings.SECRET_KEY,
                algorithm=settings.ALGORITHM
            )
            
            logger.info(f"✅ JWT created for user: {user_id}")
            return token
        
        except Exception as e:
            logger.error(f"❌ JWT creation failed: {e}")
            raise
    
    @staticmethod
    def verify_token(token: str) -> Dict:
        """
        Verify and decode JWT token
        
        Args:
            token: JWT token string
        
        Returns:
            Decoded payload containing user_id and email
        
        Raises:
            jwt.ExpiredSignatureError: Token has expired
            jwt.InvalidTokenError: Token is invalid
        
        Example:
            try:
                payload = AuthService.verify_token(token)
                user_id = payload["user_id"]
            except jwt.ExpiredSignatureError:
                # Handle expired token
            except jwt.InvalidTokenError:
                # Handle invalid token
        """
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            
            # Validate required fields
            if "user_id" not in payload:
                raise jwt.InvalidTokenError("Token missing user_id")
            
            logger.info(f"✅ Token verified for user: {payload['user_id']}")
            return payload
        
        except jwt.ExpiredSignatureError:
            logger.warning("⚠️ Token has expired")
            raise
        
        except jwt.InvalidTokenError as e:
            logger.error(f"❌ Invalid token: {e}")
            raise
    
    @staticmethod
    def decode_token_without_verification(token: str) -> Dict:
        """
        Decode token without verifying signature (for debugging only)
        
        Args:
            token: JWT token string
        
        Returns:
            Decoded payload (unverified)
        
        Warning:
            Do NOT use this for authentication!
            Only for debugging or getting user_id from expired tokens
        """
        try:
            payload = jwt.decode(
                token,
                options={"verify_signature": False}
            )
            return payload
        except Exception as e:
            logger.error(f"Token decode error: {e}")
            raise


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # Example 1: Hash password
    password = "MySecurePassword123"
    hashed = AuthService.hash_password(password)
    print(f"Hashed: {hashed}")
    
    # Example 2: Verify password
    is_valid = AuthService.verify_password(password, hashed)
    print(f"Valid: {is_valid}")  # True
    
    is_invalid = AuthService.verify_password("WrongPassword", hashed)
    print(f"Invalid: {is_invalid}")  # False
    
    # Example 3: Create JWT token
    token = AuthService.create_access_token(
        user_id="user-123",
        email="test@example.com"
    )
    print(f"Token: {token}")
    
    # Example 4: Verify JWT token
    try:
        payload = AuthService.verify_token(token)
        print(f"Payload: {payload}")
    except jwt.ExpiredSignatureError:
        print("Token expired")
    except jwt.InvalidTokenError:
        print("Invalid token")