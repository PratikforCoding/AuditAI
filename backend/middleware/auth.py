"""
JWT Authentication Middleware for FastAPI
Provides dependency injection for protected routes
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import logging
from services.auth_service import AuthService

logger = logging.getLogger(__name__)

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Dependency to get current authenticated user
    
    Usage in endpoints:
        @router.get("/protected")
        async def protected_route(user_id: str = Depends(get_current_user)):
            # user_id is automatically extracted from JWT
            return {"user_id": user_id}
    
    Args:
        credentials: Automatically extracted by FastAPI from Authorization header
    
    Returns:
        user_id: String containing the authenticated user's ID
    
    Raises:
        HTTPException 401: If token is invalid or expired
    """
    try:
        # Extract token from "Bearer <token>"
        token = credentials.credentials
        
        # Verify and decode token
        payload = AuthService.verify_token(token)
        
        # Extract user_id
        user_id = payload.get("user_id")
        
        if not user_id:
            logger.error("Token missing user_id field")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.info(f"✅ Authenticated user: {user_id}")
        return user_id
    
    except jwt.ExpiredSignatureError:
        logger.warning("⚠️ Expired token attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    except jwt.InvalidTokenError as e:
        logger.error(f"❌ Invalid token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    except Exception as e:
        logger.error(f"❌ Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_email(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Dependency to get current user's email
    
    Usage:
        @router.get("/profile")
        async def get_profile(email: str = Depends(get_current_user_email)):
            return {"email": email}
    
    Returns:
        email: User's email address from token
    """
    try:
        token = credentials.credentials
        payload = AuthService.verify_token(token)
        
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        return email
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


async def get_current_active_user(
    user_id: str = Depends(get_current_user)
) -> dict:
    """
    Get current user with database check
    
    Usage:
        @router.get("/dashboard")
        async def dashboard(user: dict = Depends(get_current_active_user)):
            # user dict contains full user info from database
            return {"welcome": user["email"]}
    
    Returns:
        user: Complete user object from database
    
    Raises:
        HTTPException 404: If user not found in database
        HTTPException 403: If user account is inactive
    """
    try:
        from models.repositories import UserRepository
        
        # Get user from database
        user = UserRepository.find_by_id(user_id)
        
        if not user:
            logger.error(f"User {user_id} not found in database")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if user is active
        if not user.is_active:
            logger.warning(f"Inactive user attempted access: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        logger.info(f"✅ Active user validated: {user_id}")
        return user.dict()
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to validate user"
        )


def require_admin(user_id: str = Depends(get_current_user)) -> str:
    """
    Dependency that requires admin role (future feature)
    
    Usage:
        @router.delete("/admin/user/{user_id}")
        async def delete_user(
            target_user_id: str,
            admin_id: str = Depends(require_admin)
        ):
            # Only admins can access this
            pass
    """
    # TODO: Implement admin check when roles are added
    # For now, just return user_id
    return user_id


# ============================================================================
# OPTIONAL: Rate Limiting Dependency
# ============================================================================

from collections import defaultdict
from datetime import datetime, timedelta

# Simple in-memory rate limiter (use Redis in production)
request_counts = defaultdict(list)

def rate_limit(max_requests: int = 100, window_minutes: int = 1):
    """
    Rate limiting dependency
    
    Usage:
        @router.post("/api/expensive-operation")
        async def expensive_op(
            user_id: str = Depends(get_current_user),
            _: None = Depends(rate_limit(max_requests=10, window_minutes=1))
        ):
            # Limited to 10 requests per minute
            pass
    """
    async def _rate_limit(user_id: str = Depends(get_current_user)):
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=window_minutes)
        
        # Clean old requests
        request_counts[user_id] = [
            req_time for req_time in request_counts[user_id]
            if req_time > window_start
        ]
        
        # Check limit
        if len(request_counts[user_id]) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: {max_requests} requests per {window_minutes} minute(s)"
            )
        
        # Add current request
        request_counts[user_id].append(now)
        
        return None
    
    return _rate_limit