"""
JWT Validation Middleware for MCP Tools
Provides authentication and authorization for MCP tools in the AI-Powered Conversational Todo System.
"""

from fastapi import HTTPException, Request, Depends
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from utils.logging import setup_logging

logger = setup_logging()

# Get JWT secret from environment
import os
JWT_SECRET = os.getenv("JWT_SECRET", "your-default-secret-key-change-in-production")


def verify_jwt_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Decode the token
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"Unexpected error during JWT verification: {str(e)}")
        raise HTTPException(status_code=401, detail="Token verification failed")


async def get_current_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> Dict[str, Any]:
    """
    Dependency to get the current user from the JWT token in the request.
    
    Args:
        credentials: HTTP authorization credentials from the request header
        
    Returns:
        Dictionary containing user information from the token
    """
    token = credentials.credentials
    user_data = verify_jwt_token(token)
    
    # Log the authentication attempt
    logger.info(f"User authenticated: {user_data.get('user_id', 'unknown')}")
    
    return user_data


def validate_user_authorization(user_data: Dict[str, Any], required_user_id: str) -> bool:
    """
    Validate that the authenticated user has permission to access resources.
    
    Args:
        user_data: User data from the JWT token
        required_user_id: The user ID that the resource belongs to
        
    Returns:
        Boolean indicating if the user is authorized
    """
    authenticated_user_id = user_data.get("user_id")
    
    if authenticated_user_id != required_user_id:
        logger.warning(f"Unauthorized access attempt: user {authenticated_user_id} tried to access resources for user {required_user_id}")
        return False
    
    return True


def require_same_user_as_token(required_user_id: str, current_user: Dict[str, Any] = Depends(get_current_user_from_token)) -> Dict[str, Any]:
    """
    Dependency to ensure the requested user ID matches the authenticated user ID.
    
    Args:
        required_user_id: The user ID that is being accessed
        current_user: Current user data from JWT token (injected)
        
    Returns:
        Current user data if authorized
        
    Raises:
        HTTPException: If user is not authorized
    """
    if not validate_user_authorization(current_user, required_user_id):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access these resources"
        )
    
    return current_user


# Example usage in an endpoint:
# 
# @app.post("/api/v1/mcp/add_task/{user_id}")
# async def add_task_endpoint(
#     user_id: str,
#     task_data: TaskCreate,
#     current_user: dict = Depends(require_same_user_as_token)
# ):
#     # The current_user will only be returned if user_id matches the token's user_id
#     # Implementation here...